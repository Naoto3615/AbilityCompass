import React, { useMemo } from 'react';
import type { PrintSettings, KanjiEntry, Theme, Difficulty } from '../types';
import { StrokeGuide } from './StrokeGuide';

interface Props {
  settings: PrintSettings;
  kanjiList: KanjiEntry[];
  /** When true, hides the preview heading (used for print-only render) */
  printMode?: boolean;
}

// Theme decorations
const ThemeDecoration: React.FC<{ theme: Theme }> = ({ theme }) => {
  if (theme === 'stars') {
    return (
      <div className="flex justify-between items-center mb-2">
        <div className="flex gap-2 text-yellow-400 text-2xl">
          <span>⭐</span><span>🌟</span><span>✨</span>
        </div>
        <div className="flex gap-2 text-yellow-400 text-2xl">
          <span>✨</span><span>🌟</span><span>⭐</span>
        </div>
      </div>
    );
  }
  if (theme === 'flowers') {
    return (
      <div className="flex justify-between items-center mb-2">
        <div className="flex gap-2 text-pink-400 text-2xl">
          <span>🌸</span><span>🌺</span><span>🌷</span>
        </div>
        <div className="flex gap-2 text-pink-400 text-2xl">
          <span>🌷</span><span>🌺</span><span>🌸</span>
        </div>
      </div>
    );
  }
  return (
    <div className="flex justify-between items-center mb-2">
      <div className="flex gap-2 text-blue-400 text-2xl">
        <span>🐠</span><span>🐙</span><span>🐚</span>
      </div>
      <div className="flex gap-2 text-blue-400 text-2xl">
        <span>🐚</span><span>🐙</span><span>🐠</span>
      </div>
    </div>
  );
};

const themeHeaderColor: Record<Theme, string> = {
  stars: 'bg-gradient-to-r from-indigo-400 via-purple-400 to-indigo-400',
  flowers: 'bg-gradient-to-r from-pink-400 via-rose-400 to-pink-400',
  ocean: 'bg-gradient-to-r from-cyan-400 via-blue-400 to-cyan-400',
};

const themeAccent: Record<Theme, string> = {
  stars: 'border-indigo-300 bg-indigo-50',
  flowers: 'border-pink-300 bg-pink-50',
  ocean: 'border-cyan-300 bg-cyan-50',
};

const themeTraceColor: Record<Theme, string> = {
  stars: '#c4b5fd',
  flowers: '#f9a8d4',
  ocean: '#67e8f9',
};

const difficultyConfig: Record<Difficulty, { label: string; color: string; emoji: string }> = {
  easy: { label: 'かんたん', color: '#bbf7d0', emoji: '🌱' },
  normal: { label: 'ふつう', color: '#fef08a', emoji: '🌼' },
  challenge: { label: 'チャレンジ', color: '#fecaca', emoji: '🔥' },
};

// Print layout sizes (~2× previous values)
const WRITING_CELL_SIZE = 100;
const TRACE_BOX_SIZE = 160;
const TRACE_FONT_SIZE = 112;
const STROKE_GUIDE_SIZE = 96;
const FILL_BLANK_SIZE = 56;

const writingCellBorder = (borderColor: string) =>
  borderColor === '#c4b5fd' ? '#a5b4fc' : borderColor === '#f9a8d4' ? '#f472b6' : '#67e8f9';

// Writing grid cells
const WritingCells: React.FC<{
  count: number;
  borderColor: string;
  layout?: 'row' | 'grid';
}> = ({ count, borderColor, layout = 'row' }) => {
  const cellStyle = {
    width: WRITING_CELL_SIZE,
    height: WRITING_CELL_SIZE,
    border: `2px solid ${writingCellBorder(borderColor)}`,
    borderRadius: 6,
    flexShrink: 0,
  } as const;

  const cell = (i: number) => (
    <div key={i} className="relative" style={cellStyle}>
      {/* Dotted cross guide lines */}
      <svg
        width={WRITING_CELL_SIZE}
        height={WRITING_CELL_SIZE}
        style={{ position: 'absolute', top: 0, left: 0, pointerEvents: 'none' }}
      >
        {/* Vertical center line */}
        <line
          x1={WRITING_CELL_SIZE / 2}
          y1={4}
          x2={WRITING_CELL_SIZE / 2}
          y2={WRITING_CELL_SIZE - 4}
          stroke="#d1d5db"
          strokeWidth={1}
          strokeDasharray="3 3"
        />
        {/* Horizontal center line */}
        <line
          x1={4}
          y1={WRITING_CELL_SIZE / 2}
          x2={WRITING_CELL_SIZE - 4}
          y2={WRITING_CELL_SIZE / 2}
          stroke="#d1d5db"
          strokeWidth={1}
          strokeDasharray="3 3"
        />
      </svg>
    </div>
  );

  if (layout === 'grid' && count === 4) {
    return (
      <div
        className="inline-grid"
        style={{
          gridTemplateColumns: `repeat(2, ${WRITING_CELL_SIZE}px)`,
          gap: 6,
        }}
      >
        {Array.from({ length: count }).map((_, i) => cell(i))}
      </div>
    );
  }

  return (
    <div className="flex flex-wrap" style={{ gap: 6 }}>
      {Array.from({ length: count }).map((_, i) => cell(i))}
    </div>
  );
};

const RALLY_CELL_COUNT = 10;
const RALLY_COLS = 5;

const themeRallyStyle: Record<
  Theme,
  { border: string; bg: string; accent: string; cellBorder: string; titleColor: string }
> = {
  stars: {
    border: '#a5b4fc',
    bg: '#eef2ff',
    accent: '#818cf8',
    cellBorder: '#c4b5fd',
    titleColor: '#4338ca',
  },
  flowers: {
    border: '#f9a8d4',
    bg: '#fdf2f8',
    accent: '#f472b6',
    cellBorder: '#fbcfe8',
    titleColor: '#be185d',
  },
  ocean: {
    border: '#67e8f9',
    bg: '#ecfeff',
    accent: '#22d3ee',
    cellBorder: '#a5f3fc',
    titleColor: '#0e7490',
  },
};

const RallyStarDeco: React.FC<{ color: string }> = ({ color }) => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill={color} aria-hidden="true">
    <path d="M7 0.5L8.4 5.1L13 5.1L9.3 8.1L10.7 12.7L7 9.7L3.3 12.7L4.7 8.1L1 5.1L5.6 5.1Z" />
  </svg>
);

const RallyFlowerDeco: React.FC<{ color: string }> = ({ color }) => (
  <svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">
    <circle cx="7" cy="4" r="2.2" fill={color} opacity="0.85" />
    <circle cx="4.2" cy="6.5" r="2.2" fill={color} opacity="0.85" />
    <circle cx="9.8" cy="6.5" r="2.2" fill={color} opacity="0.85" />
    <circle cx="5.5" cy="9.8" r="2.2" fill={color} opacity="0.85" />
    <circle cx="8.5" cy="9.8" r="2.2" fill={color} opacity="0.85" />
    <circle cx="7" cy="7" r="1.6" fill="#fef08a" />
  </svg>
);

const RallyWaveDeco: React.FC<{ color: string }> = ({ color }) => (
  <svg width="28" height="10" viewBox="0 0 28 10" aria-hidden="true">
    <path
      d="M0 6 C4 2, 8 2, 14 6 C20 10, 24 10, 28 6"
      fill="none"
      stroke={color}
      strokeWidth="1.5"
      strokeLinecap="round"
    />
    <path
      d="M0 9 C4 5, 8 5, 14 9 C20 13, 24 13, 28 9"
      fill="none"
      stroke={color}
      strokeWidth="1.5"
      strokeLinecap="round"
      opacity="0.6"
    />
  </svg>
);

const RallyDecoration: React.FC<{ theme: Theme; color: string }> = ({ theme, color }) => {
  if (theme === 'stars') return <RallyStarDeco color={color} />;
  if (theme === 'flowers') return <RallyFlowerDeco color={color} />;
  return <RallyWaveDeco color={color} />;
};

const StampRallyArea: React.FC<{ theme: Theme; childName: string }> = ({ theme, childName }) => {
  const style = themeRallyStyle[theme];
  const title = childName
    ? `${childName}ちゃんの スタンプラリー`
    : 'がんばりスタンプ';

  return (
    <div
      className="stamp-rally-area mt-4 pt-3"
      style={{ breakInside: 'avoid', pageBreakInside: 'avoid' }}
    >
      <div
        className="rounded-2xl px-4 py-3"
        style={{
          border: `2px solid ${style.border}`,
          background: style.bg,
        }}
      >
        <div className="flex items-center justify-center gap-2 mb-1">
          <RallyDecoration theme={theme} color={style.accent} />
          <p
            className="text-sm font-black text-center"
            style={{ color: style.titleColor }}
          >
            {title}
          </p>
          <RallyDecoration theme={theme} color={style.accent} />
        </div>
        {!childName && (
          <p className="text-xs text-center mb-2 font-bold" style={{ color: style.accent }}>
            スタンプラリー
          </p>
        )}
        <p className="text-xs text-center mb-3 text-gray-500">
          れんしゅうができたら マスにスタンプを はろう！
        </p>
        <div
          className="mx-auto"
          style={{
            display: 'grid',
            gridTemplateColumns: `repeat(${RALLY_COLS}, 44px)`,
            gap: 8,
            justifyContent: 'center',
          }}
        >
          {Array.from({ length: RALLY_CELL_COUNT }).map((_, i) => (
            <div
              key={i}
              className="stamp-rally-cell relative"
              style={{ borderColor: style.cellBorder }}
            >
              <span
                className="absolute top-0.5 left-1 text-[9px] font-bold leading-none"
                style={{ color: style.accent, opacity: 0.7 }}
              >
                {i + 1}
              </span>
            </div>
          ))}
        </div>
        <div className="flex justify-center gap-3 mt-2 opacity-70">
          <RallyDecoration theme={theme} color={style.accent} />
          <RallyDecoration theme={theme} color={style.accent} />
          <RallyDecoration theme={theme} color={style.accent} />
        </div>
      </div>
    </div>
  );
};

// Individual problem card
const ProblemCard: React.FC<{
  number: number;
  kanji: KanjiEntry;
  settings: PrintSettings;
}> = ({ number, kanji, settings }) => {
  const { problemType, theme, showDifficultyBadge, strokeOrderKanjiIds } = settings;
  const showStrokeOrder = strokeOrderKanjiIds.includes(kanji.id);
  const diff = difficultyConfig[kanji.difficulty];
  const traceColor = themeTraceColor[theme];
  const accentClass = themeAccent[theme];

  return (
    <div
      className={`rounded-2xl border-2 p-3 print-problem-card ${accentClass} relative overflow-hidden`}
      style={{ breakInside: 'avoid', pageBreakInside: 'avoid' }}
    >
      {/* Problem number */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <div
            className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-black text-sm ${
              theme === 'stars' ? 'bg-indigo-400' : theme === 'flowers' ? 'bg-pink-400' : 'bg-cyan-500'
            }`}
          >
            {number}
          </div>
          {showDifficultyBadge && (
            <span
              className="text-xs px-2 py-0.5 rounded-full font-bold"
              style={{ background: diff.color }}
            >
              {diff.emoji} {diff.label}
            </span>
          )}
        </div>
      </div>

      {/* Problem content */}
      {problemType === 'trace' && (
        <div className="flex flex-col gap-3">
          <div className="flex items-start gap-4 flex-wrap">
            {showStrokeOrder && (
              <div className="shrink-0 flex flex-col items-center">
                <p className="text-xs text-gray-500 mb-1 text-center">かきじゅん</p>
                <StrokeGuide kanji={kanji.kanji} size={STROKE_GUIDE_SIZE} />
              </div>
            )}
            <div className="shrink-0">
              <p className="text-xs text-gray-500 mb-1 text-center">なぞってみよう</p>
              <div
                className="flex items-center justify-center rounded-xl border-2 border-dashed"
                style={{
                  width: TRACE_BOX_SIZE,
                  height: TRACE_BOX_SIZE,
                  borderColor: traceColor,
                }}
              >
                <span
                  className="font-black select-none trace-kanji"
                  style={{ fontSize: TRACE_FONT_SIZE, color: traceColor, lineHeight: 1 }}
                >
                  {kanji.kanji}
                </span>
              </div>
              <p className="text-xs text-center mt-1" style={{ color: traceColor }}>
                {kanji.reading}
              </p>
            </div>
          </div>
          <div>
            <p className="text-xs text-gray-500 mb-1">じぶんで書いてみよう</p>
            <WritingCells count={3} borderColor={traceColor} layout="row" />
          </div>
        </div>
      )}

      {problemType === 'reading' && (
        <div className="flex flex-col gap-3">
          <div className="shrink-0">
            <p className="text-xs text-gray-500 mb-1 text-center">よみがな</p>
            <div
              className="inline-block px-5 py-3 rounded-xl border-2 font-bold text-2xl text-gray-700"
              style={{ borderColor: traceColor, background: 'white' }}
            >
              {kanji.reading}
            </div>
          </div>
          <div>
            <p className="text-xs text-gray-500 mb-1">この漢字を書こう！</p>
            <WritingCells count={3} borderColor={traceColor} />
          </div>
        </div>
      )}

      {problemType === 'fill' && (
        <div>
          <p className="text-xs text-gray-500 mb-2">□に漢字を書こう！</p>
          <div className="flex items-center gap-2 flex-wrap">
            <div className="text-lg font-bold text-gray-700">
              {kanji.example.replace(kanji.kanji, '')}の□に入る漢字は？
            </div>
          </div>
          <div className="flex items-center gap-2 mt-2">
            <p className="text-base font-bold text-gray-600">
              {kanji.example.includes(kanji.kanji)
                ? kanji.example.split(kanji.kanji).map((part, i, arr) => (
                    <React.Fragment key={i}>
                      {part}
                      {i < arr.length - 1 && (
                        <span
                          className="inline-block mx-1 align-bottom"
                          style={{
                            width: FILL_BLANK_SIZE,
                            height: FILL_BLANK_SIZE,
                            border: `2px solid ${traceColor}`,
                            borderRadius: 6,
                            verticalAlign: 'middle',
                          }}
                        />
                      )}
                    </React.Fragment>
                  ))
                : kanji.example}
            </p>
          </div>
          <p className="text-xs text-gray-400 mt-1">（{kanji.exampleReading}）</p>
          <div className="mt-2">
            <WritingCells count={3} borderColor={traceColor} />
          </div>
        </div>
      )}
    </div>
  );
};

export const PrintPreview: React.FC<Props> = ({ settings, kanjiList, printMode = false }) => {
  const { childName, theme, problemCount, selectedKanjiIds, randomize } = settings;

  const problems = useMemo(() => {
    let pool =
      selectedKanjiIds.length > 0
        ? kanjiList.filter((k) => selectedKanjiIds.includes(k.id))
        : [...kanjiList];

    if (pool.length === 0) pool = [...kanjiList];

    if (randomize) {
      pool = [...pool].sort(() => Math.random() - 0.5);
    }

    return pool.slice(0, problemCount);
  }, [kanjiList, selectedKanjiIds, problemCount, randomize]);

  const today = new Date().toLocaleDateString('ja-JP', {
    year: 'numeric', month: 'long', day: 'numeric', weekday: 'long',
  });

  return (
    <div>
      {!printMode && (
        <div className="no-print mb-3">
          <h2 className="text-xl font-black text-gray-700 flex items-center gap-2">
            <span>👀</span> プレビュー
          </h2>
          {settings.showStampRally && (
            <p className="text-sm text-orange-600 font-bold mt-1 flex items-center gap-1">
              <span>👇</span>
              スタンプラリー欄は プリントの いちばん下に あります。下まで スクロールして ね！
            </p>
          )}
        </div>
      )}
      {/* A4 preview / print wrapper */}
      <div className={printMode ? undefined : 'overflow-auto'}>
        <div
          id="print-area"
          style={{
            width: '210mm',
            minHeight: '297mm',
            background: 'white',
            padding: '12mm',
            margin: '0 auto',
            boxShadow: '0 4px 32px rgba(0,0,0,0.12)',
            borderRadius: 8,
            fontFamily: "'Noto Sans JP', sans-serif",
          }}
        >
          {/* Header decoration */}
          <ThemeDecoration theme={theme} />

          {/* Title bar */}
          <div
            className={`rounded-2xl px-6 py-3 mb-4 text-center text-white ${themeHeaderColor[theme]}`}
          >
            <h1 className="text-2xl font-black tracking-wider">
              {childName ? `${childName}ちゃんだけの特別プリント` : 'かんじれんしゅうプリント'}
            </h1>
            <p className="text-sm opacity-90 mt-0.5 font-medium">
              {settings.problemType === 'trace'
                ? '✏️ なぞり書き練習'
                : settings.problemType === 'reading'
                ? '📖 よみがなから書く'
                : '🔤 れいぶん穴埋め'}{' '}
              ／ {today}
            </p>
          </div>

          {/* Name & score row */}
          <div className="flex items-center gap-4 mb-4">
            <div
              className="flex items-center gap-2 px-4 py-2 rounded-xl border-2"
              style={{ borderColor: themeTraceColor[theme], flex: 1 }}
            >
              <span className="text-sm font-bold text-gray-600">なまえ：</span>
              <div className="flex-1 h-6 border-b-2 border-dashed border-gray-300" />
            </div>
            <div
              className="flex items-center gap-2 px-4 py-2 rounded-xl border-2"
              style={{ borderColor: themeTraceColor[theme] }}
            >
              <span className="text-sm font-bold text-gray-600">てん：</span>
              <div className="w-16 h-6 border-b-2 border-dashed border-gray-300" />
              <span className="text-sm text-gray-600">てん</span>
            </div>
          </div>

          {/* Problems — trace uses 1 column; reading/fill use 2 columns when ≤4 problems */}
          <div
            className="grid gap-3"
            style={{
              gridTemplateColumns:
                settings.problemType === 'trace' || problems.length > 4 ? '1fr' : '1fr 1fr',
            }}
          >
            {problems.map((k, i) => (
              <ProblemCard
                key={k.id}
                number={i + 1}
                kanji={k}
                settings={settings}
              />
            ))}
          </div>

          {/* Stamp rally area */}
          {settings.showStampRally && (
            <StampRallyArea theme={theme} childName={childName} />
          )}

          {/* Footer */}
          <div className="mt-4 text-center">
            <p className="text-xs text-gray-400">
              ✨ よくがんばりました！ ✨　かんじれんしゅうプリント
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
