# Retriever
# Finds candidate knowledge objects by matching extracted entities.

import os
import re


def load_domain(domain_dir):
    result = []
    kdir = os.path.join(domain_dir, "knowledge")
    if not os.path.isdir(kdir):
        return result
    for fname in sorted(os.listdir(kdir)):
        if fname.endswith(".md"):
            path = os.path.join(kdir, fname)
            obj = _parse_object(path)
            if obj:
                result.append(obj)
    return result


def _parse_object(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    identity = _extract_section(content, "Identity")
    metadata = _extract_section(content, "Metadata")
    semantic = _extract_section(content, "Semantic Layer")

    if not identity:
        return None

    tags = _parse_list(metadata, "tags")
    if not tags:
        tags = _parse_list(identity, "tags")

    return {
        "content": content,
        "path": path,
        "id": _parse_field(identity, "id"),
        "title": _parse_field(identity, "title"),
        "type": _parse_field(identity, "type"),
        "tags": tags,
        "semantic": semantic,
    }


def _extract_section(content, name):
    m = re.search(r"^## " + name + r"\n[ \t]*\n(.+?)(?=\n## |\Z)", content, re.DOTALL | re.MULTILINE)
    if not m:
        m = re.search(r"^## " + name + r"\n(.+?)(?=\n## |\Z)", content, re.DOTALL | re.MULTILINE)
    return m.group(1).strip() if m else ""


def _parse_field(section, field):
    m = re.search(r"^- " + field + r":\s*(.*)", section, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _parse_list(section, field):
    m = re.search(r"^- " + field + r":\s*\[(.*)\]", section, re.MULTILINE)
    if m:
        items = [i.strip().strip("\"").strip("'") for i in m.group(1).split(",")]
        return [i for i in items if i]
    return []


def retrieve(entities, knowledge_objects):
    scored = []
    for obj in knowledge_objects:
        max_entity_score = 0.0
        all_matched_on = []

        obj_id = obj["id"].lower()
        obj_title = obj["title"].lower()
        obj_tags = [t.lower() for t in obj["tags"]]
        obj_semantic = obj["semantic"].lower()

        for entity in entities:
            e = entity.lower()
            entity_score = 0.0
            entity_matches = []

            if e == obj_id:
                entity_score += 1.0
                entity_matches.append("exact_id")
            elif obj_id.startswith(e) or e.startswith(obj_id):
                entity_score += 0.8
                entity_matches.append("id_prefix_match")
            elif e in obj_id:
                entity_score += 0.3
                entity_matches.append("partial_id")
            if e in obj_title:
                entity_score += 0.8
                entity_matches.append("title_match")
            for tag in obj_tags:
                if e == tag:
                    entity_score += 0.7
                    entity_matches.append("tag_match")
                    break
                if e in tag or tag in e:
                    entity_score += 0.5
                    entity_matches.append("tag_match")
                    break
            if e in obj_semantic:
                entity_score += 0.4
                entity_matches.append("semantic_match")

            if entity_score > max_entity_score:
                max_entity_score = entity_score
            all_matched_on.extend(entity_matches)

        if max_entity_score > 0:
            scored.append({
                "id": obj["id"],
                "title": obj["title"],
                "type": obj["type"],
                "score": round(max_entity_score, 2),
                "matched_on": all_matched_on,
                "content": obj["content"],
                "semantic": obj["semantic"],
                "tags": obj["tags"],
            })

    def _tie_break(item):
        has_id_match = "exact_id" in item["matched_on"] or "id_prefix_match" in item["matched_on"]
        has_title_tag = "title_match" in item["matched_on"] or "tag_match" in item["matched_on"]
        if has_id_match:
            return 0
        if has_title_tag:
            return 1
        return 2

    scored.sort(key=lambda x: (x["score"], -_tie_break(x)), reverse=True)
    return scored
