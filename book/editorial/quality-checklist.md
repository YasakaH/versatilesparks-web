# Quality Checklist

Before any chapter is considered frozen, it must pass every check below.

## Content

- [ ] Production story included (realistic incident, one failure, one lesson)
- [ ] Mental model explicitly stated
- [ ] Learning objectives listed (3-5 for V1, 5-7 for V2)
- [ ] Previously box at chapter start
- [ ] Why This Exists section answers the business motivation
- [ ] Common mistakes section included (3-5 V1, 6-10 V2)
- [ ] Reflection questions included (3 V1, 5-7 V2)
- [ ] Production checklist at chapter end
- [ ] Chapter connections box referencing Stable IDs and modules
- [ ] Chapter summary (max 1 paragraph)
- [ ] Next chapter preview (2-3 lines)

## Diagrams

- [ ] At least 1 architecture diagram
- [ ] At least 1 decision diagram or comparison table
- [ ] No two diagrams of the same type adjacent
- [ ] Every diagram has a caption
- [ ] All Mermaid blocks render correctly
- [ ] Diagram adds information not present in text

## Recipes

- [ ] Recipe follows its tier's section requirements
- [ ] Stable ID present and in recipe-index.md
- [ ] File path referenced correctly in chapter text
- [ ] Code includes imports (no hidden imports)
- [ ] Code is runnable (or labeled as excerpt)
- [ ] Failure modes included for Tier 1 recipes (minimum 3)
- [ ] Decision table included for Tier 1 recipes
- [ ] Production rule included
- [ ] Business example used (never example.com)
- [ ] Deprecated APIs not taught

## Cross-References

- [ ] All Stable IDs are valid (exist in recipe-index.md)
- [ ] All module paths exist under common/
- [ ] All recipe file paths exist
- [ ] Chapter dependencies listed correctly
- [ ] "Next Chapter" link points to the next chapter file

## Writing

- [ ] No prohibited words (amazing, simply, basically, very, robust)
- [ ] No marketing language or hyperbole
- [ ] Sentences under 35 words
- [ ] Paragraphs under 5 lines
- [ ] Lists under 7 bullets
- [ ] Consistent terminology (profile ≠ user-data-dir)
- [ ] Production Rule formatted as blockquote with "> **Production Rule:**"
- [ ] Engineering Notes under 100 words
- [ ] Analogy count: max 1 per major section

## Technical Accuracy

- [ ] Code compiles/validates (Python syntax check)
- [ ] Module imports are correct
- [ ] API calls use current (non-deprecated) versions
- [ ] nodriver syntax verified against 0.50.3
- [ ] CDP event references are correct

## Metadata

- [ ] Chapter file named correctly (`chapter-NN.md`)
- [ ] Recipe files named with correct numbers
- [ ] Recipe index updated with any new Stable IDs
- [ ] Architecture map updated if chapter structure changed
