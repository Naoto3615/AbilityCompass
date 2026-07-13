import React, { useState } from 'react';
import type { KanjiEntry, Difficulty } from '../types';
import { defaultKanji } from '../data/kanji2nd';

interface Props {
  kanjiList: KanjiEntry[];
  onUpdate: (list: KanjiEntry[]) => void;
}

const difficultyLabel: Record<Difficulty, string> = {
  easy: 'かんたん',
  normal: 'ふつう',
  challenge: 'チャレンジ',
};

const difficultyColor: Record<Difficulty, string> = {
  easy: 'bg-green-100 text-green-700 border-green-300',
  normal: 'bg-yellow-100 text-yellow-700 border-yellow-300',
  challenge: 'bg-red-100 text-red-700 border-red-300',
};

const emptyEntry = (): Omit<KanjiEntry, 'id'> => ({
  kanji: '',
  reading: '',
  meaning: '',
  example: '',
  exampleReading: '',
  difficulty: 'normal',
});

export const KanjiManager: React.FC<Props> = ({ kanjiList, onUpdate }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterDifficulty, setFilterDifficulty] = useState<Difficulty | 'all'>('all');
  const [isAdding, setIsAdding] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [form, setForm] = useState(emptyEntry());
  const [editForm, setEditForm] = useState<KanjiEntry | null>(null);

  const filtered = kanjiList.filter((k) => {
    const matchSearch =
      !searchQuery ||
      k.kanji.includes(searchQuery) ||
      k.reading.includes(searchQuery) ||
      k.meaning.includes(searchQuery);
    const matchDiff = filterDifficulty === 'all' || k.difficulty === filterDifficulty;
    return matchSearch && matchDiff;
  });

  const handleAdd = () => {
    if (!form.kanji.trim()) return;
    const newEntry: KanjiEntry = {
      ...form,
      id: `custom-${Date.now()}`,
    };
    onUpdate([...kanjiList, newEntry]);
    setForm(emptyEntry());
    setIsAdding(false);
  };

  const handleDelete = (id: string) => {
    onUpdate(kanjiList.filter((k) => k.id !== id));
  };

  const handleEditSave = () => {
    if (!editForm) return;
    onUpdate(kanjiList.map((k) => (k.id === editForm.id ? editForm : k)));
    setEditingId(null);
    setEditForm(null);
  };

  const handleReset = () => {
    if (window.confirm('デフォルトの漢字リストに戻しますか？\n追加した漢字は消えます。')) {
      onUpdate(defaultKanji);
    }
  };

  return (
    <div className="no-print bg-white rounded-3xl shadow-lg border-2 border-pink-200 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
        <h2 className="text-xl font-black text-pink-600 flex items-center gap-2">
          <span>📚</span> かんじリスト
          <span className="text-sm font-normal text-gray-500 ml-1">({kanjiList.length}字)</span>
        </h2>
        <div className="flex gap-2">
          <button
            onClick={handleReset}
            className="text-xs px-3 py-1.5 rounded-full border border-gray-300 text-gray-600 hover:bg-gray-50 transition-colors"
          >
            リセット
          </button>
          <button
            onClick={() => { setIsAdding(true); setForm(emptyEntry()); }}
            className="text-sm px-4 py-2 rounded-full bg-pink-400 text-white font-bold hover:bg-pink-500 transition-colors shadow-sm"
          >
            ＋ 追加
          </button>
        </div>
      </div>

      {/* Search and filter */}
      <div className="flex gap-2 mb-4 flex-wrap">
        <input
          type="text"
          placeholder="🔍 かんじをさがす..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1 min-w-[140px] rounded-full border-2 border-pink-200 px-4 py-1.5 text-sm focus:outline-none focus:border-pink-400"
        />
        <select
          value={filterDifficulty}
          onChange={(e) => setFilterDifficulty(e.target.value as Difficulty | 'all')}
          className="rounded-full border-2 border-purple-200 px-3 py-1.5 text-sm focus:outline-none focus:border-purple-400 bg-white"
        >
          <option value="all">すべて</option>
          <option value="easy">かんたん</option>
          <option value="normal">ふつう</option>
          <option value="challenge">チャレンジ</option>
        </select>
      </div>

      {/* Add form */}
      {isAdding && (
        <div className="mb-4 p-4 bg-pink-50 rounded-2xl border-2 border-pink-200">
          <h3 className="font-bold text-pink-600 mb-3">✏️ あたらしい漢字を追加</h3>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
            <input
              placeholder="漢字 *"
              value={form.kanji}
              onChange={(e) => setForm({ ...form, kanji: e.target.value })}
              className="rounded-xl border-2 border-pink-200 px-3 py-2 text-xl text-center font-bold focus:outline-none focus:border-pink-400"
            />
            <input
              placeholder="よみがな"
              value={form.reading}
              onChange={(e) => setForm({ ...form, reading: e.target.value })}
              className="rounded-xl border-2 border-pink-200 px-3 py-2 text-sm focus:outline-none focus:border-pink-400"
            />
            <input
              placeholder="いみ"
              value={form.meaning}
              onChange={(e) => setForm({ ...form, meaning: e.target.value })}
              className="rounded-xl border-2 border-pink-200 px-3 py-2 text-sm focus:outline-none focus:border-pink-400"
            />
            <input
              placeholder="れいぶん"
              value={form.example}
              onChange={(e) => setForm({ ...form, example: e.target.value })}
              className="rounded-xl border-2 border-pink-200 px-3 py-2 text-sm focus:outline-none focus:border-pink-400 col-span-2"
            />
            <select
              value={form.difficulty}
              onChange={(e) => setForm({ ...form, difficulty: e.target.value as Difficulty })}
              className="rounded-xl border-2 border-pink-200 px-3 py-2 text-sm focus:outline-none focus:border-pink-400 bg-white"
            >
              <option value="easy">かんたん</option>
              <option value="normal">ふつう</option>
              <option value="challenge">チャレンジ</option>
            </select>
          </div>
          <div className="flex gap-2 mt-3 justify-end">
            <button
              onClick={() => setIsAdding(false)}
              className="px-4 py-2 rounded-full border border-gray-300 text-gray-600 text-sm hover:bg-gray-50"
            >
              キャンセル
            </button>
            <button
              onClick={handleAdd}
              disabled={!form.kanji.trim()}
              className="px-4 py-2 rounded-full bg-pink-400 text-white font-bold text-sm hover:bg-pink-500 disabled:opacity-50"
            >
              追加する
            </button>
          </div>
        </div>
      )}

      {/* Kanji grid */}
      <div className="max-h-96 overflow-y-auto pr-1">
        <div className="grid grid-cols-1 gap-2">
          {filtered.length === 0 && (
            <p className="text-center text-gray-400 py-8">みつかりませんでした 🔍</p>
          )}
          {filtered.map((k) => (
            <div key={k.id}>
              {editingId === k.id && editForm ? (
                <div className="p-3 bg-yellow-50 rounded-2xl border-2 border-yellow-200">
                  <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 mb-2">
                    <input
                      value={editForm.kanji}
                      onChange={(e) => setEditForm({ ...editForm, kanji: e.target.value })}
                      className="rounded-xl border-2 border-yellow-300 px-3 py-1.5 text-xl text-center font-bold focus:outline-none"
                    />
                    <input
                      value={editForm.reading}
                      onChange={(e) => setEditForm({ ...editForm, reading: e.target.value })}
                      placeholder="よみがな"
                      className="rounded-xl border-2 border-yellow-300 px-3 py-1.5 text-sm focus:outline-none"
                    />
                    <input
                      value={editForm.example}
                      onChange={(e) => setEditForm({ ...editForm, example: e.target.value })}
                      placeholder="れいぶん"
                      className="rounded-xl border-2 border-yellow-300 px-3 py-1.5 text-sm focus:outline-none col-span-2 sm:col-span-1"
                    />
                    <select
                      value={editForm.difficulty}
                      onChange={(e) => setEditForm({ ...editForm, difficulty: e.target.value as Difficulty })}
                      className="rounded-xl border-2 border-yellow-300 px-3 py-1.5 text-sm bg-white focus:outline-none"
                    >
                      <option value="easy">かんたん</option>
                      <option value="normal">ふつう</option>
                      <option value="challenge">チャレンジ</option>
                    </select>
                  </div>
                  <div className="flex gap-2 justify-end">
                    <button onClick={() => { setEditingId(null); setEditForm(null); }} className="px-3 py-1 rounded-full border border-gray-300 text-gray-600 text-xs hover:bg-gray-50">キャンセル</button>
                    <button onClick={handleEditSave} className="px-3 py-1 rounded-full bg-yellow-400 text-white font-bold text-xs hover:bg-yellow-500">保存</button>
                  </div>
                </div>
              ) : (
                <div className="flex items-center gap-3 p-3 rounded-2xl hover:bg-pink-50 transition-colors group">
                  <span className="text-3xl font-black text-gray-800 w-10 text-center shrink-0">{k.kanji}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-sm text-gray-600">{k.reading}</span>
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${difficultyColor[k.difficulty]}`}>
                        {difficultyLabel[k.difficulty]}
                      </span>
                    </div>
                    <p className="text-xs text-gray-400 truncate">{k.example}</p>
                  </div>
                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
                    <button
                      onClick={() => { setEditingId(k.id); setEditForm({ ...k }); setIsAdding(false); }}
                      className="p-1.5 rounded-full hover:bg-yellow-100 text-yellow-600 transition-colors"
                      title="編集"
                    >
                      ✏️
                    </button>
                    <button
                      onClick={() => handleDelete(k.id)}
                      className="p-1.5 rounded-full hover:bg-red-100 text-red-500 transition-colors"
                      title="削除"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
