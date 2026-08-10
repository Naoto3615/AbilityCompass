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
  const [strokeSearchQuery, setStrokeSearchQuery] = useState('');
  const strokeOrderKanjiIds = settings.strokeOrderKanjiIds ?? [];
  const isTraceMode = settings.problemType === 'trace';

  const printTargetKanji =
    settings.selectedKanjiIds.length > 0
      ? kanjiList.filter((k) => settings.selectedKanjiIds.includes(k.id))
      : kanjiList;

  const filterKanji = (list: KanjiEntry[], query: string) => {
    if (!query.trim()) return list;
    const q = query.trim().toLowerCase();
    return list.filter(
      (k) =>
        k.kanji.includes(query) ||
        k.reading.includes(query) ||
        (k.onyomi && k.onyomi.toLowerCase().includes(q)) ||
        (k.kunyomi && k.kunyomi.includes(query)) ||
        k.example.includes(query)
    );
  };

  const filteredKanjiList = filterKanji(kanjiList, searchQuery);
  const filteredStrokeKanjiList = filterKanji(printTargetKanji, strokeSearchQuery);

  const toggleStrokeOrder = (id: string) => {
    const selected = strokeOrderKanjiIds.includes(id);
    const ids = selected
      ? strokeOrderKanjiIds.filter((i) => i !== id)
      : [...strokeOrderKanjiIds, id];
    set('strokeOrderKanjiIds', ids);
  };

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
        <div className="flex flex-wrap gap-2 justify-center">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((n) => (
            <button
              key={n}
              onClick={() => set('problemCount', n)}
              className={`w-12 h-12 rounded-2xl font-black text-lg transition-all border-2 ${
                settings.problemCount === n
                  ? 'bg-pink-400 text-white border-pink-400 shadow-md scale-110'
                  : 'bg-white text-pink-400 border-pink-200 hover:border-pink-400 hover:bg-pink-50'
              }`}
            >
              {n}
            </button>
          ))}
        </div>
        <p className="text-xs text-gray-400 text-center mt-3">
          えらんだかず: <span className="font-bold text-pink-500">{settings.problemCount}もん</span>
        </p>
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
            placeholder="漢字・音読み・訓読みで さがす"
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

      {/* Stroke order selection (trace mode only) */}
      {isTraceMode && (
        <div className="bg-white rounded-3xl shadow-lg border-2 border-teal-200 p-6">
          <h2 className="text-xl font-black text-teal-600 mb-1 flex items-center gap-2">
            <span>✍️</span> かきじゅんを ひょうじする かんじ
          </h2>
          <p className="text-xs text-gray-500 mb-3">
            えらんだ漢字だけ、書き順ガイドが表示されます
          </p>

          <div className="flex gap-2 mb-3 flex-wrap">
            <button
              onClick={() =>
                set(
                  'strokeOrderKanjiIds',
                  printTargetKanji.filter((k) => k.difficulty === 'challenge').map((k) => k.id)
                )
              }
              className="text-xs px-3 py-1.5 rounded-full bg-red-100 text-red-600 font-bold hover:bg-red-200 transition-colors"
            >
              🔥 むずかしさ チャレンジ のみ
            </button>
            <button
              onClick={() => set('strokeOrderKanjiIds', printTargetKanji.map((k) => k.id))}
              className="text-xs px-3 py-1.5 rounded-full bg-teal-100 text-teal-600 font-bold hover:bg-teal-200 transition-colors"
            >
              えらんだ かんじすべて
            </button>
            <button
              onClick={() => set('strokeOrderKanjiIds', [])}
              className="text-xs px-3 py-1.5 rounded-full bg-gray-100 text-gray-600 font-bold hover:bg-gray-200 transition-colors"
            >
              すべて けす
            </button>
          </div>

          <div className="relative mb-3">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-teal-300 text-base pointer-events-none">🔍</span>
            <input
              type="text"
              placeholder="漢字・音読み・訓読みで さがす"
              value={strokeSearchQuery}
              onChange={(e) => setStrokeSearchQuery(e.target.value)}
              className="w-full rounded-2xl border-2 border-teal-200 pl-9 pr-9 py-2 text-sm font-bold focus:outline-none focus:border-teal-400 placeholder-teal-200 bg-teal-50 transition-colors"
            />
            {strokeSearchQuery && (
              <button
                onClick={() => setStrokeSearchQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-teal-300 hover:text-teal-500 transition-colors text-lg leading-none"
                aria-label="検索をクリア"
              >
                ×
              </button>
            )}
          </div>

          <div className="max-h-48 overflow-y-auto">
            {filteredStrokeKanjiList.length === 0 ? (
              <p className="text-center text-teal-400 font-bold py-6 text-sm">
                🔍 みつかりませんでした
              </p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {filteredStrokeKanjiList.map((k) => {
                  const selected = strokeOrderKanjiIds.includes(k.id);
                  return (
                    <button
                      key={k.id}
                      onClick={() => toggleStrokeOrder(k.id)}
                      className={`relative w-11 h-11 rounded-xl text-xl font-black transition-all border-2 ${
                        selected
                          ? 'bg-teal-400 text-white border-teal-500 shadow-md scale-110'
                          : 'bg-white text-gray-700 border-gray-200 hover:border-teal-300 hover:bg-teal-50'
                      }`}
                      title={`${k.kanji}（${k.reading}）`}
                    >
                      {selected && (
                        <span className="absolute -top-1 -right-1 w-4 h-4 bg-teal-500 rounded-full text-white text-[10px] flex items-center justify-center leading-none">
                          ✓
                        </span>
                      )}
                      {k.kanji}
                    </button>
                  );
                })}
              </div>
            )}
          </div>
          <p className="text-xs text-gray-400 mt-2">
            {strokeOrderKanjiIds.length > 0
              ? `${strokeOrderKanjiIds.length}字に書き順を表示`
              : '書き順なし（なぞり文字のみ）'}
          </p>
        </div>
      )}

      {/* Options */}
      <div className="bg-white rounded-3xl shadow-lg border-2 border-orange-200 p-6">
        <h2 className="text-xl font-black text-orange-600 mb-4 flex items-center gap-2">
          <span>⚙️</span> オプション
        </h2>
        <div className="space-y-3">
          <label className="flex items-center gap-3 cursor-pointer group">
            <div
              onClick={() => set('showStampRally', !settings.showStampRally)}
              className={`w-12 h-6 rounded-full transition-colors ${settings.showStampRally ? 'bg-orange-400' : 'bg-gray-200'}`}
            >
              <div className={`w-5 h-5 bg-white rounded-full shadow mt-0.5 transition-transform ${settings.showStampRally ? 'translate-x-6.5' : 'translate-x-0.5'}`} />
            </div>
            <span className="text-sm font-bold text-gray-700 group-hover:text-orange-500 transition-colors">
              スタンプラリー欄を いれる
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
