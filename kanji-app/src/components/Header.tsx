import React from 'react';

const StarIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
  </svg>
);

const HeartIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
  </svg>
);

const FlowerIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <circle cx="12" cy="12" r="3" />
    <ellipse cx="12" cy="6" rx="2" ry="3" />
    <ellipse cx="12" cy="18" rx="2" ry="3" />
    <ellipse cx="6" cy="12" rx="3" ry="2" />
    <ellipse cx="18" cy="12" rx="3" ry="2" />
    <ellipse cx="7.76" cy="7.76" rx="2" ry="3" transform="rotate(45 7.76 7.76)" />
    <ellipse cx="16.24" cy="16.24" rx="2" ry="3" transform="rotate(45 16.24 16.24)" />
    <ellipse cx="16.24" cy="7.76" rx="2" ry="3" transform="rotate(-45 16.24 7.76)" />
    <ellipse cx="7.76" cy="16.24" rx="2" ry="3" transform="rotate(-45 7.76 16.24)" />
  </svg>
);

export const Header: React.FC = () => {
  return (
    <header className="no-print bg-gradient-to-r from-pink-400 via-purple-400 to-pink-400 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex gap-1">
              <span className="text-yellow-300 sparkle"><StarIcon /></span>
              <span className="text-pink-200 float" style={{ animationDelay: '0.5s' }}><HeartIcon /></span>
              <span className="text-green-300 sparkle" style={{ animationDelay: '1s' }}><FlowerIcon /></span>
            </div>
            <div>
              <h1 className="text-2xl font-black text-white drop-shadow-md tracking-wide">
                かんじれんしゅうプリント
              </h1>
              <p className="text-pink-100 text-sm font-medium">
                ✨ たのしく かんじを おぼえよう！✨
              </p>
            </div>
          </div>
          <div className="flex gap-1 items-center">
            <span className="text-yellow-300 sparkle" style={{ animationDelay: '0.3s' }}><StarIcon /></span>
            <span className="text-pink-200 float" style={{ animationDelay: '0.8s' }}><HeartIcon /></span>
            <span className="text-yellow-300 sparkle" style={{ animationDelay: '1.3s' }}><StarIcon /></span>
          </div>
        </div>
      </div>
    </header>
  );
};
