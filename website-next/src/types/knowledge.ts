export type Difficulty = "Beginner" | "Intermediate" | "Advanced";

export interface ConceptRecipeRef {
    id: string;
    title: string;
    slug: string;
    book: string;
    difficulty: Difficulty;
    environment: string[];
}

export interface ConceptBookRef {
    id: string;
    title: string;
    slug: string;
    version: string;
}

export interface ConceptArticleRef {
    slug: string;
    title: string;
    description: string;
    tags: string[];
}

export interface ConceptProblemRef {
    id: string;
    title: string;
    slug: string;
    error_patterns: string[];
    severity: "common" | "rare" | "critical";
}

export interface RecipeConceptRef {
    id: string;
    title: string;
    slug: string;
    summary: string;
    difficulty: Difficulty;
}

export interface RecipeBookRef {
    id: string;
    title: string;
    slug: string;
    version: string;
}

export interface Concept {
    id: string;
    title: string;
    summary: string;
    difficulty: Difficulty;
    requires: string[];
    used_by: string[];
    tags: string[];
    aliases: string[];
    introduced: string;
    updated: string;
    deprecated: boolean;
    compatible_with: string;
    last_reviewed: string;
    slug: string;
    body: string;
    related: string[];
    group: string;
    next_steps: string[];
    recipes: ConceptRecipeRef[];
    books: ConceptBookRef[];
    problems: ConceptProblemRef[];
    articles: ConceptArticleRef[];
}

export interface Recipe {
    id: string;
    title: string;
    concepts: string[];
    difficulty: Difficulty;
    environment: string[];
    downloads: string[];
    book: string;
    slug: string;
    body: string;
    summary?: string;
    prerequisites: string[];
    conceptObjects: RecipeConceptRef[];
    bookObject: RecipeBookRef | null;
}

export interface Book {
    id: string;
    title: string;
    subtitle: string;
    price_usd: number;
    price_inr: number;
    version: string;
    released: string;
    gumroad_url: string;
    formats: string[];
    slug: string;
    body: string;
    summary?: string;
}

export interface Problem {
    id: string;
    title: string;
    slug: string;
    error_patterns: string[];
    severity: "common" | "rare" | "critical";
    concept: string;
    description: string;
    body: string;
    conceptObject?: RecipeConceptRef;
}

export interface KnowledgeBase {
    concepts: Concept[];
    recipes: Recipe[];
    books: Book[];
    problems: Problem[];
}
