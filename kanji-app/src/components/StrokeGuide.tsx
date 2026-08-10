import React, { useRef, useLayoutEffect, useState, useMemo, useId } from 'react';
import { strokeOrderData } from '../data/strokeOrder';

interface Props {
  kanji: string;
  /** Display size in pixels. Default: 96 */
  size?: number;
}

const KANJI_SIZE = 109;

/** Pastel colors for stroke highlights — cycles through the palette */
const STROKE_PALETTE = [
  'rgba(251,113,133,0.42)',  // rose
  'rgba(96,165,250,0.42)',   // blue
  'rgba(74,222,128,0.42)',   // green
  'rgba(251,146,60,0.42)',   // orange
  'rgba(167,139,250,0.42)',  // violet
  'rgba(245,158,11,0.42)',   // amber
  'rgba(20,184,166,0.42)',   // teal
  'rgba(236,72,153,0.42)',   // pink
  'rgba(99,102,241,0.42)',   // indigo
  'rgba(34,211,238,0.42)',   // cyan
];

const HIGHLIGHT_WIDTH = 12;    // width of the colored stroke blob
const BASE_STROKE_WIDTH = 1.2; // thin gray base kanji
const START_DOT_R = 2.2;       // radius of the black dot at stroke start
const ARROW_SIZE = 5;          // half-size of arrowhead

/** Get the unit outward vector from center for a point */
function outwardUnit(x: number, y: number): [number, number] {
  const cx = KANJI_SIZE / 2;
  const cy = KANJI_SIZE / 2;
  const dx = x - cx;
  const dy = y - cy;
  const len = Math.sqrt(dx * dx + dy * dy) || 1;
  return [dx / len, dy / len];
}

/** Clamp a coordinate to stay within the SVG viewbox */
function clamp(v: number, lo: number, hi: number): number {
  return Math.max(lo, Math.min(hi, v));
}

interface ArrowInfo {
  /** x,y of the arrow tip */
  tipX: number;
  tipY: number;
  /** angle in radians, pointing in the direction of stroke travel */
  angle: number;
}

interface NumberPos {
  x: number;
  y: number;
}

interface StrokeRenderInfo {
  arrow: ArrowInfo | null;
  numPos: NumberPos;
}

function computeStrokeInfo(
  el: SVGPathElement,
  startPt: { x: number; y: number },
): StrokeRenderInfo {
  const len = el.getTotalLength();

  // --- Number position ---
  // Place number slightly outside the stroke start, away from kanji center
  const [ox, oy] = outwardUnit(startPt.x, startPt.y);
  const numDist = 9;
  const numPos: NumberPos = {
    x: clamp(startPt.x + ox * numDist, 3, KANJI_SIZE - 3),
    y: clamp(startPt.y + oy * numDist, 3, KANJI_SIZE - 3),
  };

  // --- Arrow (direction indicator) ---
  if (len < 8) return { arrow: null, numPos };

  // Sample around 55% of the path to find direction
  const t = Math.min(0.55, (len - 4) / len);
  const d = len * t;
  const p0 = el.getPointAtLength(Math.max(0, d - 2));
  const p1 = el.getPointAtLength(Math.min(len, d + 2));
  const ax = p1.x - p0.x;
  const ay = p1.y - p0.y;
  const alen = Math.sqrt(ax * ax + ay * ay);
  if (alen < 0.001) return { arrow: null, numPos };

  const mid = el.getPointAtLength(d);
  const arrow: ArrowInfo = {
    tipX: mid.x,
    tipY: mid.y,
    angle: Math.atan2(ay, ax),
  };

  return { arrow, numPos };
}

function ArrowHead({
  tip,
  angle,
  color,
}: {
  tip: [number, number];
  angle: number;
  color: string;
}) {
  const [tx, ty] = tip;
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  // Three points of a triangle centered at tip, pointing in `angle` direction
  const size = ARROW_SIZE;
  // tip point
  const x0 = tx + cos * size * 0.6;
  const y0 = ty + sin * size * 0.6;
  // back-left
  const x1 = tx - cos * size * 0.5 + sin * size * 0.5;
  const y1 = ty - sin * size * 0.5 - cos * size * 0.5;
  // back-right
  const x2 = tx - cos * size * 0.5 - sin * size * 0.5;
  const y2 = ty - sin * size * 0.5 + cos * size * 0.5;

  return (
    <polygon
      points={`${x0},${y0} ${x1},${y1} ${x2},${y2}`}
      fill={color}
      stroke="none"
    />
  );
}

/**
 * Stroke-order guide inspired by kakikata.maripo.org:
 * - All strokes shown as thin gray base
 * - Each stroke highlighted with a wide semi-transparent pastel band
 * - Plain number near stroke start, black dot AT stroke start
 * - Direction arrowhead on the stroke
 *
 * KanjiVG data © Ulrich Apel — CC BY-SA 3.0
 */
export const StrokeGuide: React.FC<Props> = ({ kanji, size = 96 }) => {
  const data = strokeOrderData[kanji];
  const pathRefs = useRef<(SVGPathElement | null)[]>([]);
  const [renderInfos, setRenderInfos] = useState<StrokeRenderInfo[]>([]);
  const gradId = useId().replace(/:/g, '');

  const paths = useMemo(() => data?.paths ?? [], [data]);
  const starts = useMemo(() => data?.starts ?? [], [data]);

  useLayoutEffect(() => {
    if (!data || data.paths.length === 0) {
      setRenderInfos([]);
      return;
    }
    const infos = pathRefs.current.map((el, i) => {
      if (!el || !starts[i]) return { arrow: null, numPos: { x: 10, y: 10 } };
      return computeStrokeInfo(el, starts[i]);
    });
    setRenderInfos(infos);
  }, [data, kanji, starts]);

  // Fallback when no data
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
          borderRadius: 6,
          background: '#fafafa',
        }}
      >
        <span style={{ fontSize: size * 0.5, color: 'rgba(0,0,0,0.1)', userSelect: 'none' }}>
          {kanji}
        </span>
        <span style={{ fontSize: 7, color: '#9ca3af', marginTop: 2, textAlign: 'center' }}>
          かきじゅんは教科書で確認しよう
        </span>
      </div>
    );
  }

  const strokeCount = paths.length;
  // Font size for stroke numbers — scale with stroke count
  const numFontSize = strokeCount >= 14 ? 4.8 : strokeCount >= 10 ? 5.2 : 5.8;

  return (
    <div
      title={`${kanji} の書き順`}
      style={{
        width: size,
        height: size,
        flexShrink: 0,
        background: '#fff',
        borderRadius: 4,
        position: 'relative',
      }}
    >
      <svg
        viewBox={`0 0 ${KANJI_SIZE} ${KANJI_SIZE}`}
        width={size}
        height={size}
        xmlns="http://www.w3.org/2000/svg"
        style={{ display: 'block', overflow: 'visible', background: '#fff' }}
        aria-label={`${kanji}の書き順`}
      >
        <defs>
          {/* Unique clip for this instance */}
          <clipPath id={`clip-${gradId}`}>
            <rect x={0} y={0} width={KANJI_SIZE} height={KANJI_SIZE} />
          </clipPath>
        </defs>

        {/* 1. Thin gray base strokes (all at once for context) */}
        <g clipPath={`url(#clip-${gradId})`}>
          {paths.map((d, i) => (
            <path
              key={`base-${i}`}
              ref={(el) => { pathRefs.current[i] = el; }}
              d={d}
              fill="none"
              stroke="#d1d5db"
              strokeWidth={BASE_STROKE_WIDTH}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          ))}

          {/* 2. Colored highlight blobs per stroke */}
          {paths.map((d, i) => {
            const color = STROKE_PALETTE[i % STROKE_PALETTE.length];
            return (
              <path
                key={`hl-${i}`}
                d={d}
                fill="none"
                stroke={color}
                strokeWidth={HIGHLIGHT_WIDTH}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            );
          })}

          {/* 3. Direction arrows on each stroke */}
          {renderInfos.map((info, i) => {
            if (!info.arrow) return null;
            const color = STROKE_PALETTE[i % STROKE_PALETTE.length]
              .replace(/[\d.]+\)$/, '0.9)'); // more opaque for arrow
            return (
              <ArrowHead
                key={`arrow-${i}`}
                tip={[info.arrow.tipX, info.arrow.tipY]}
                angle={info.arrow.angle}
                color={color}
              />
            );
          })}

          {/* 4. Black dot at stroke start */}
          {starts.map((pt, i) => {
            if (!pt) return null;
            return (
              <circle
                key={`dot-${i}`}
                cx={pt.x}
                cy={pt.y}
                r={START_DOT_R}
                fill="#1f2937"
              />
            );
          })}
        </g>

        {/* 5. Stroke numbers — plain text, positioned outside stroke */}
        {/* These are outside the clipPath so numbers near edge remain visible */}
        {renderInfos.map((info, i) => (
          <text
            key={`num-${i}`}
            x={info.numPos.x}
            y={info.numPos.y}
            textAnchor="middle"
            dominantBaseline="central"
            fontSize={numFontSize}
            fontWeight="700"
            fill="#1f2937"
            style={{ fontFamily: 'sans-serif', userSelect: 'none' }}
          >
            {i + 1}
          </text>
        ))}
      </svg>
    </div>
  );
};
