import React from 'react';
import { strokeOrderData } from '../data/strokeOrder';

interface Props {
  kanji: string;
  /** Display size in pixels (rendered as a square). Default: 72 */
  size?: number;
}

/**
 * Renders a stroke-order guide for a kanji using KanjiVG data.
 * Each stroke is drawn in light gray, with a circled number at its starting point.
 * Falls back to a simple gray kanji with a note if no stroke data is available.
 *
 * KanjiVG data © Ulrich Apel — CC BY-SA 3.0
 */
export const StrokeGuide: React.FC<Props> = ({ kanji, size = 72 }) => {
  const data = strokeOrderData[kanji];

  if (!data || data.paths.length === 0) {
    return (
      <div
        style={{
          width: size,
          height: size,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          border: '1px dashed #d1d5db',
          borderRadius: 4,
          background: '#f9fafb',
        }}
      >
        <span
          style={{
            fontSize: size * 0.55,
            color: 'rgba(0,0,0,0.12)',
            lineHeight: 1,
            fontWeight: 900,
            userSelect: 'none',
          }}
        >
          {kanji}
        </span>
        <span
          style={{
            fontSize: 7,
            color: '#9ca3af',
            textAlign: 'center',
            marginTop: 2,
            lineHeight: 1.2,
            maxWidth: size - 4,
          }}
        >
          かきじゅんは教科書で確認しよう
        </span>
      </div>
    );
  }

  const { paths, starts } = data;
  const VIEWBOX = 109;
  // Number circle radius in viewBox units
  const R = 5.5;

  return (
    <div
      title={`${kanji} の書き順`}
      style={{ width: size, height: size, flexShrink: 0 }}
    >
      <svg
        viewBox={`0 0 ${VIEWBOX} ${VIEWBOX}`}
        width={size}
        height={size}
        xmlns="http://www.w3.org/2000/svg"
        style={{ display: 'block', overflow: 'visible' }}
        aria-label={`${kanji}の書き順`}
      >
        {/* Stroke paths — light gray */}
        {paths.map((d, i) => (
          <path
            key={`stroke-${i}`}
            d={d}
            fill="none"
            stroke="#b0b0b0"
            strokeWidth={3}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        ))}

        {/* Stroke order numbers */}
        {starts.map((pt, i) => {
          if (!pt) return null;
          // Clamp number circle so it stays within viewBox
          const cx = Math.min(Math.max(pt.x, R + 1), VIEWBOX - R - 1);
          const cy = Math.min(Math.max(pt.y, R + 1), VIEWBOX - R - 1);
          return (
            <g key={`num-${i}`}>
              <circle cx={cx} cy={cy} r={R} fill="#ef4444" opacity={0.85} />
              <text
                x={cx}
                y={cy}
                textAnchor="middle"
                dominantBaseline="central"
                fontSize={paths.length >= 10 ? 5.5 : 6.5}
                fontWeight="bold"
                fill="white"
                style={{ fontFamily: 'sans-serif', userSelect: 'none' }}
              >
                {i + 1}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};
