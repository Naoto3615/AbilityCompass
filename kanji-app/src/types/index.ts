export interface KanjiEntry {
  id: string;
  kanji: string;
  reading: string;
  onyomi?: string;
  kunyomi?: string;
  meaning: string;
  example: string;
  exampleReading: string;
  difficulty: 'easy' | 'normal' | 'challenge';
}

export type ProblemType = 'trace' | 'reading' | 'fill';
export type Theme = 'stars' | 'flowers' | 'ocean';
export type Difficulty = 'easy' | 'normal' | 'challenge';

export interface PrintSettings {
  childName: string;
  problemType: ProblemType;
  problemCount: number;
  theme: Theme;
  showStampRally: boolean;
  showDifficultyBadge: boolean;
  selectedKanjiIds: string[];
  strokeOrderKanjiIds: string[];
  randomize: boolean;
}
