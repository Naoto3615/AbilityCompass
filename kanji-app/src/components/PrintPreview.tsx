import React, { useMemo } from 'react';
import type { PrintSettings, KanjiEntry, Theme, Difficulty } from '../types';
import { StrokeGuide } from './StrokeGuide';

interface Props {
  settings: PrintSettings;
  kanjiList: KanjiEntry[];
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

// Writing grid cells
const WritingCells: React.FC<{ count: number; borderColor: string }> = ({ count, borderColor }) => (
  <div className="flex gap-1">
    {Array.from({ length: count }).map((_, i) => (
      <div
        key={i}
        className="relative"
        style={{
          width: 48,
          height: 48,
          border: `2px solid ${borderColor === '#c4b5fd' ? '#a5b4fc' : borderColor === '#f9a8d4' ? '#f472b6' : '#67e8f9'}`,
          borderRadius: 4,
          flexShrink: 0,
        }}
      >
        {/* center cross guides */}
        <div style={{
          position: 'absolute', top: 0, left: '50%', width: 1, height: '100%',
          background: '#e5e7eb', transform: 'translateX(-50%)',
        }} />
        <div style={{
          position: 'absolute', top: '50%', left: 0, width: '100%', height: 1,
          background: '#e5e7eb', transform: 'translateY(-50%)',
        }} />
      </div>
    ))}
  </div>
);

// Stamp area
const StampArea: React.FC<{ theme: Theme }> = ({ theme }) => {
  const emojis = theme === 'stars' ? ['⭐', '🌟', '✨'] : theme === 'flowers' ? ['🌸', '🌺', '🌷'] : ['🐠', '🐙', '🐚'];
  return (
    <div className="mt-4 pt-3 border-t-2 border-dashed border-gray-300">
      <p className="text-xs text-gray-500 text-center mb-2 font-bold">✨ ごほうびスタンプをはろう！</p>
      <div className="flex justify-center gap-4">
        {emojis.map((e, i) => (
          <div
            key={i}
            style={{
              width: 56,
              height: 56,
              border: '2px dashed #d1d5db',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 10,
              color: '#9ca3af',
              flexDirection: 'column',
            }}
          >
            <span style={{ fontSize: 18, opacity: 0.15 }}>{e}</span>
          </div>
        ))}
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
  const { problemType, theme, showDifficultyBadge } = settings;
  const diff = difficultyConfig[kanji.difficulty];
  const traceColor = themeTraceColor[theme];
  const accentClass = themeAccent[theme];

  return (
    <div
      className={`rounded-2xl border-2 p-4 ${accentClass} relative overflow-hidden`}
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
        <div className="flex items-start gap-4">
          {/* Trace kanji */}
          <div className="shrink-0">
            <p className="text-xs text-gray-500 mb-1 text-center">なぞってみよう</p>
            <div
              className="w-20 h-20 flex items-center justify-center rounded-xl border-2 border-dashed"
              style={{ borderColor: traceColor }}
            >
              <span
                className="font-black select-none"
                style={{ fontSize: 56, color: traceColor, lineHeight: 1 }}
              >
                {kanji.kanji}
              </span>
            </div>
            <p className="text-xs text-center mt-1" style={{ color: traceColor }}>
              {kanji.reading}
            </p>
          </div>
          {/* Write boxes */}
          <div>
            <p className="text-xs text-gray-500 mb-1">じぶんで書いてみよう</p>
            <WritingCells count={4} borderColor={traceColor} />
          </div>
        </div>
      )}

      {problemType === 'reading' && (
        <div className="flex items-start gap-4">
          <div className="shrink-0">
            <p className="text-xs text-gray-500 mb-1 text-center">よみがな</p>
            <div
              className="px-4 py-3 rounded-xl border-2 font-bold text-xl text-gray-700"
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
                            width: 28, height: 28,
                            border: `2px solid ${traceColor}`,
                            borderRadius: 4,
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

export const PrintPreview: React.FC<Props> = ({ settings, kanjiList }) => {
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
    <div className="no-print">
      <h2 className="text-xl font-black text-gray-700 mb-3 flex items-center gap-2">
        <span>👀</span> プレビュー
      </h2>
      {/* A4 preview wrapper */}
      <div className="overflow-auto">
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

          {/* Problems */}
          <div className="grid grid-cols-1 gap-4" style={{ gridTemplateColumns: problems.length <= 4 ? '1fr 1fr' : '1fr 1fr' }}>
            {problems.map((k, i) => (
              <ProblemCard
                key={k.id}
                number={i + 1}
                kanji={k}
                settings={settings}
              />
            ))}
          </div>

          {/* Stamp area */}
          {settings.showStampArea && <StampArea theme={theme} />}

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
