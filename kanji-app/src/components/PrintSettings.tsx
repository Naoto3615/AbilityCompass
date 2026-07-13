import React, { useState } from 'react';
import type { PrintSettings as PrintSettingsType, ProblemType, Theme, KanjiEntry } from '../types';

interface Props {
  settings: PrintSettingsType;
  kanjiList: KanjiEntry[];
  onUpdate: (s: PrintSettingsType) => void;
  onPrint: () => void;
}

const themes: { value: Theme; label: string; emoji: string; desc: string }[] = [
  { value: 'stars', label: 'ほしぞら', emoji: '⭐', desc: 'きらきらな星たちと一緒に！' },
  { value: 'flowers', label: 'おはなばたけ', emoji: '🌸', desc: 'お花がいっぱいのプリント！' },
  { value: 'ocean', label: 'うみのなかま', emoji: '🐠', desc: '海の生き物たちと遊ぼう！' },
];

const problemTypes: { value: ProblemType; label: string; emoji: string; desc: string }[] = [
  { value: 'trace', label: 'なぞり書き', emoji: '✏️', desc: 'うすい文字をなぞって書く' },
  { value: 'reading', label: 'よみがなから書く', emoji: '📖', desc: 'よみがなを見て書く' },
  { value: 'fill', label: 'れいぶん穴埋め', emoji: '🔤', desc: '文の□に漢字を書く' },
];

export const PrintSettings: React.FC<Props> = ({ settings, kanjiList, onUpdate, onPrint }) => {
  const set = <K extends keyof PrintSettingsType>(key: K, value: PrintSettingsType[K]) =>
    onUpdate({ ...settings, [key]: value });

  const [searchQuery, setSearchQuery] = useState('');

  const filteredKanjiList = searchQuery.trim()
    ? kanjiList.filter(
        (k) =>
          k.kanji.includes(searchQuery) ||
          k.reading.includes(searchQuery) ||
          k.example.includes(searchQuery)
      )
    : kanjiList;

  return (
    <div className="no-print space-y-4">
      {/* Child name */}
      <div className="bg-white rounded-3xl shadow-lg border-2 border-purple-200 p-6">
        <h2 className="text-xl font-black text-purple-600 mb-4 flex items-center gap-2">
          <span>👧</span> こどもの名前
        </h2>
        <div className="relative">
          <input
            type="text"
            placeholder="なまえをいれてね"
            value={settings.childName}
            onChange={(e) => set('childName', e.target.value)}
            className="w-full rounded-2xl border-2 border-purple-200 px-4 py-3 text-lg font-bold focus:outline-none focus:border-purple-400 placeholder-purple-200"
          />
          {settings.childName && (
            <p className="mt-2 text-sm text-purple-500 font-medium">
              ✨ 「{settings.childName}ちゃんだけの特別プリント」になるよ！
            </p>
          )}
        </div>
      </div>

      {/* Theme selection */}
      <div className="bg-white rounded-3xl shadow-lg border-2 border-yellow-200 p-6">
        <h2 className="text-xl font-black text-yellow-600 mb-4 flex items-center gap-2">
          <span>🎨</span> テーマをえらぼう
        </h2>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          {themes.map((t) => (
            <button
              key={t.value}
              onClick={() => set('theme', t.value)}
              className={`p-4 rounded-2xl border-2 text-left transition-all ${
                settings.theme === t.value
                  ? 'border-yellow-400 bg-yellow-50 shadow-md scale-[1.02]'
                  : 'border-gray-200 hover:border-yellow-200 hover:bg-yellow-50'
              }`}
            >
              <div className="text-2xl mb-1">{t.emoji}</div>
              <div className="font-bold text-gray-800 text-sm">{t.label}</div>
              <div className="text-xs text-gray-500 mt-0.5">{t.desc}</div>
              {settings.theme === t.value && (
                <div className="mt-1 text-xs text-yellow-600 font-bold">✓ えらばれてるよ</div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Problem type */}
      <div className="bg-white rounded-3xl shadow-lg border-2 border-green-200 p-6">
        <h2 className="text-xl font-black text-green-600 mb-4 flex items-center gap-2">
          <span>📝</span> もんだいのかたち
        </h2>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          {problemTypes.map((pt) => (
            <button
              key={pt.value}
              onClick={() => set('problemType', pt.value)}
              className={`p-4 rounded-2xl border-2 text-left transition-all ${
                settings.problemType === pt.value
                  ? 'border-green-400 bg-green-50 shadow-md scale-[1.02]'
                  : 'border-gray-200 hover:border-green-200 hover:bg-green-50'
              }`}
            >
              <div className="text-2xl mb-1">{pt.emoji}</div>
              <div className="font-bold text-gray-800 text-sm">{pt.label}</div>
              <div className="text-xs text-gray-500 mt-0.5">{pt.desc}</div>
              {settings.problemType === pt.value && (
                <div className="mt-1 text-xs text-green-600 font-bold">✓ えらばれてるよ</div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Problem count */}
      <div className="bg-white rounded-3xl shadow-lg border-2 border-blue-200 p-6">
        <h2 className="text-xl font-black text-blue-600 mb-4 flex items-center gap-2">
          <span>🔢</span> もんだいのかず
        </h2>
        <div className="flex items-center gap-4">
          <input
            type="range"
            min={3}
            max={8}
            value={settings.problemCount}
            onChange={(e) => set('problemCount', Number(e.target.value))}
            className="flex-1 accent-pink-400"
          />
          <span className="text-3xl font-black text-pink-500 w-16 text-center">
            {settings.problemCount}<span className="text-lg">もん</span>
          </span>
        </div>
        <div className="flex justify-between text-xs text-gray-400 px-1 mt-1">
          <span>3もん</span>
          <span>8もん</span>
        </div>
      </div>

      {/* Kanji selection */}
      <div className="bg-white rounded-3xl shadow-lg border-2 border-pink-200 p-6">
        <h2 className="text-xl font-black text-pink-600 mb-1 flex items-center gap-2">
          <span>✨</span> かんじをえらぶ
        </h2>
        <p className="text-xs text-gray-500 mb-3">
          えらばないと、ランダムに{settings.problemCount}字えらびます
        </p>

        <div className="flex gap-2 mb-3 flex-wrap">
          <button
            onClick={() => set('selectedKanjiIds', kanjiList.map((k) => k.id))}
            className="text-xs px-3 py-1.5 rounded-full bg-pink-100 text-pink-600 font-bold hover:bg-pink-200 transition-colors"
          >
            すべてえらぶ
          </button>
          <button
            onClick={() => set('selectedKanjiIds', [])}
            className="text-xs px-3 py-1.5 rounded-full bg-gray-100 text-gray-600 font-bold hover:bg-gray-200 transition-colors"
          >
            クリア
          </button>
        </div>

        <div className="relative mb-3">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-pink-300 text-base pointer-events-none">🔍</span>
          <input
            type="text"
            placeholder="漢字やよみがなで さがす"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full rounded-2xl border-2 border-pink-200 pl-9 pr-9 py-2 text-sm font-bold focus:outline-none focus:border-pink-400 placeholder-pink-200 bg-pink-50 transition-colors"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-pink-300 hover:text-pink-500 transition-colors text-lg leading-none"
              aria-label="検索をクリア"
            >
              ×
            </button>
          )}
        </div>

        <div className="max-h-48 overflow-y-auto">
          {filteredKanjiList.length === 0 ? (
            <p className="text-center text-pink-400 font-bold py-6 text-sm">
              🔍 みつかりませんでした
            </p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {filteredKanjiList.map((k) => {
                const selected = settings.selectedKanjiIds.includes(k.id);
                return (
                  <button
                    key={k.id}
                    onClick={() => {
                      const ids = selected
                        ? settings.selectedKanjiIds.filter((id) => id !== k.id)
                        : [...settings.selectedKanjiIds, k.id];
                      set('selectedKanjiIds', ids);
                    }}
                    className={`w-11 h-11 rounded-xl text-xl font-black transition-all border-2 ${
                      selected
                        ? 'bg-pink-400 text-white border-pink-500 shadow-md scale-110'
                        : 'bg-white text-gray-700 border-gray-200 hover:border-pink-300 hover:bg-pink-50'
                    }`}
                    title={`${k.kanji}（${k.reading}）`}
                  >
                    {k.kanji}
                  </button>
                );
              })}
            </div>
          )}
        </div>
        <p className="text-xs text-gray-400 mt-2">
          {settings.selectedKanjiIds.length > 0
            ? `${settings.selectedKanjiIds.length}字えらんでいます`
            : 'えらんでいません（ランダム）'}
        </p>
      </div>

      {/* Options */}
      <div className="bg-white rounded-3xl shadow-lg border-2 border-orange-200 p-6">
        <h2 className="text-xl font-black text-orange-600 mb-4 flex items-center gap-2">
          <span>⚙️</span> オプション
        </h2>
        <div className="space-y-3">
          <label className="flex items-center gap-3 cursor-pointer group">
            <div
              onClick={() => set('showStampArea', !settings.showStampArea)}
              className={`w-12 h-6 rounded-full transition-colors ${settings.showStampArea ? 'bg-orange-400' : 'bg-gray-200'}`}
            >
              <div className={`w-5 h-5 bg-white rounded-full shadow mt-0.5 transition-transform ${settings.showStampArea ? 'translate-x-6.5' : 'translate-x-0.5'}`} />
            </div>
            <span className="text-sm font-bold text-gray-700 group-hover:text-orange-500 transition-colors">
              🌟 ごほうびスタンプ欄を印刷する
            </span>
          </label>
          <label className="flex items-center gap-3 cursor-pointer group">
            <div
              onClick={() => set('showDifficultyBadge', !settings.showDifficultyBadge)}
              className={`w-12 h-6 rounded-full transition-colors ${settings.showDifficultyBadge ? 'bg-orange-400' : 'bg-gray-200'}`}
            >
              <div className={`w-5 h-5 bg-white rounded-full shadow mt-0.5 transition-transform ${settings.showDifficultyBadge ? 'translate-x-6.5' : 'translate-x-0.5'}`} />
            </div>
            <span className="text-sm font-bold text-gray-700 group-hover:text-orange-500 transition-colors">
              🏅 むずかしさバッジを表示する
            </span>
          </label>
          <label className="flex items-center gap-3 cursor-pointer group">
            <div
              onClick={() => set('randomize', !settings.randomize)}
              className={`w-12 h-6 rounded-full transition-colors ${settings.randomize ? 'bg-orange-400' : 'bg-gray-200'}`}
            >
              <div className={`w-5 h-5 bg-white rounded-full shadow mt-0.5 transition-transform ${settings.randomize ? 'translate-x-6.5' : 'translate-x-0.5'}`} />
            </div>
            <span className="text-sm font-bold text-gray-700 group-hover:text-orange-500 transition-colors">
              🎲 毎回ランダムに並び替え
            </span>
          </label>
        </div>
      </div>

      {/* Print button */}
      <button
        onClick={onPrint}
        className="w-full py-5 rounded-3xl bg-gradient-to-r from-pink-400 to-purple-400 text-white text-xl font-black shadow-lg hover:shadow-xl transition-all hover:scale-[1.02] active:scale-[0.98]"
      >
        🖨️ プリントする！
      </button>
    </div>
  );
};
