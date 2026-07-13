import React, { useMemo, useRef, useLayoutEffect, useState, useId } from 'react';
import { strokeOrderData } from '../data/strokeOrder';

interface Props {
  kanji: string;
  /** Display size in pixels (rendered as a square). Default: 96 */
  size?: number;
}

/** KanjiVG coordinate space for stroke paths. */
const KANJI_SIZE = 109;

const ARROW_COLOR = '#dc2626';
const STROKE_COLOR = '#1a1a1a';
const STROKE_WIDTH = 6.5;
const ARROW_STROKE_WIDTH = 1.5;
const MIN_ARROW_LENGTH = 10;
const SAME_START_THRESHOLD = 8;

interface LabelLayout {
  strokeIndex: number;
  startX: number;
  startY: number;
  labelX: number;
  labelY: number;
  radius: number;
}

interface SequenceGroup {
  strokeIndices: number[];
}

interface ParallelArrow {
  pathD: string;
}

function getCircleRadius(strokeCount: number): number {
  if (strokeCount >= 15) return 4;
  if (strokeCount >= 12) return 4.2;
  if (strokeCount >= 8) return 4.5;
  return 5;
}

function getFontSize(strokeCount: number): number {
  if (strokeCount >= 15) return 4.8;
  if (strokeCount >= 12) return 5;
  if (strokeCount >= 8) return 5.2;
  return 5.8;
}

function startDistance(
  a: { x: number; y: number },
  b: { x: number; y: number },
): number {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  return Math.sqrt(dx * dx + dy * dy);
}

function findSameStartGroups(starts: { x: number; y: number }[]): number[][] {
  const n = starts.length;
  const parent = Array.from({ length: n }, (_, i) => i);

  const find = (i: number): number => {
    let root = i;
    while (parent[root] !== root) {
      parent[root] = parent[parent[root]];
      root = parent[root];
    }
    return root;
  };

  const union = (i: number, j: number) => {
    const pi = find(i);
    const pj = find(j);
    if (pi !== pj) parent[pi] = pj;
  };

  for (let i = 0; i < n; i++) {
    if (!starts[i]) continue;
    for (let j = i + 1; j < n; j++) {
      if (!starts[j]) continue;
      if (startDistance(starts[i], starts[j]) <= SAME_START_THRESHOLD) {
        union(i, j);
      }
    }
  }

  const groupMap = new Map<number, number[]>();
  for (let i = 0; i < n; i++) {
    if (!starts[i]) continue;
    const root = find(i);
    if (!groupMap.has(root)) groupMap.set(root, []);
    groupMap.get(root)!.push(i);
  }

  return Array.from(groupMap.values()).filter((members) => members.length > 1);
}

const LABEL_COLLISION_PADDING = 2;

function getOutwardUnitVector(point: { x: number; y: number }): { x: number; y: number } {
  const cx = KANJI_SIZE / 2;
  const cy = KANJI_SIZE / 2;
  const dx = point.x - cx;
  const dy = point.y - cy;
  const len = Math.sqrt(dx * dx + dy * dy);
  if (len < 0.001) return { x: 0, y: -1 };
  return { x: dx / len, y: dy / len };
}

function rotateVector(
  v: { x: number; y: number },
  angleDeg: number,
): { x: number; y: number } {
  const rad = (angleDeg * Math.PI) / 180;
  const cos = Math.cos(rad);
  const sin = Math.sin(rad);
  return {
    x: v.x * cos - v.y * sin,
    y: v.x * sin + v.y * cos,
  };
}

function getFanAngles(groupSize: number): number[] {
  if (groupSize <= 1) return [0];
  if (groupSize === 2) return [-25, 25];
  if (groupSize === 3) return [-30, 0, 30];
  const halfSpan = 25 + (groupSize - 2) * 10;
  const step = (2 * halfSpan) / (groupSize - 1);
  return Array.from({ length: groupSize }, (_, i) => -halfSpan + step * i);
}

function getFanOffsetFromStart(
  position: number,
  groupSize: number,
  startPoint: { x: number; y: number },
  spread: number,
): { x: number; y: number } {
  const angles = getFanAngles(groupSize);
  const outward = getOutwardUnitVector(startPoint);
  const dir = rotateVector(outward, angles[position] ?? 0);
  return { x: dir.x * spread, y: dir.y * spread };
}

function getLabelOffsetFromStart(
  startPoint: { x: number; y: number },
  baseRadius: number,
): { x: number; y: number } {
  const outward = getOutwardUnitVector(startPoint);
  const distance = baseRadius + 4;
  return { x: outward.x * distance, y: outward.y * distance };
}

function clampToViewBox(
  x: number,
  y: number,
  padding: number,
): { x: number; y: number } {
  return {
    x: Math.max(padding, Math.min(KANJI_SIZE - padding, x)),
    y: Math.max(padding, Math.min(KANJI_SIZE - padding, y)),
  };
}

function labelsOverlap(a: LabelLayout, b: LabelLayout): boolean {
  const dx = a.labelX - b.labelX;
  const dy = a.labelY - b.labelY;
  const dist = Math.sqrt(dx * dx + dy * dy);
  return dist < a.radius + b.radius + LABEL_COLLISION_PADDING;
}

function findOverlappingGroups(layouts: LabelLayout[]): number[][] {
  const n = layouts.length;
  const parent = Array.from({ length: n }, (_, i) => i);

  const find = (i: number): number => {
    let root = i;
    while (parent[root] !== root) {
      parent[root] = parent[parent[root]];
      root = parent[root];
    }
    return root;
  };

  const union = (i: number, j: number) => {
    const pi = find(i);
    const pj = find(j);
    if (pi !== pj) parent[pi] = pj;
  };

  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      if (labelsOverlap(layouts[i], layouts[j])) {
        union(i, j);
      }
    }
  }

  const groupMap = new Map<number, number[]>();
  for (let i = 0; i < n; i++) {
    const root = find(i);
    if (!groupMap.has(root)) groupMap.set(root, []);
    groupMap.get(root)!.push(i);
  }

  return Array.from(groupMap.values()).filter((members) => members.length > 1);
}

function applyFanOffsets(
  layouts: LabelLayout[],
  layoutIndices: number[],
  spread: number,
): void {
  const sorted = [...layoutIndices].sort(
    (a, b) => layouts[a].strokeIndex - layouts[b].strokeIndex,
  );

  sorted.forEach((layoutIdx, position) => {
    const layout = layouts[layoutIdx];
    const baseOffset = getLabelOffsetFromStart(
      { x: layout.startX, y: layout.startY },
      layout.radius,
    );
    const offset = getFanOffsetFromStart(
      position,
      sorted.length,
      { x: layout.startX, y: layout.startY },
      spread,
    );
    layouts[layoutIdx] = {
      ...layout,
      labelX: layout.startX + baseOffset.x + offset.x,
      labelY: layout.startY + baseOffset.y + offset.y,
      radius: position > 0 ? layout.radius * 0.88 : layout.radius,
    };
  });
}

function resolveLabelCollisions(
  layouts: LabelLayout[],
  baseRadius: number,
): LabelLayout[] {
  const result = layouts.map((layout) => ({ ...layout }));

  for (let iteration = 0; iteration < 6; iteration++) {
    const overlapGroups = findOverlappingGroups(result);
    if (overlapGroups.length === 0) break;

    const spread = baseRadius * (3.0 + iteration * 0.4);
    for (const group of overlapGroups) {
      applyFanOffsets(result, group, spread);
    }
  }

  return result;
}

function clampLabelLayouts(layouts: LabelLayout[]): LabelLayout[] {
  return layouts.map((layout) => {
    const padding = layout.radius + 0.5;
    const clamped = clampToViewBox(layout.labelX, layout.labelY, padding);
    return { ...layout, labelX: clamped.x, labelY: clamped.y };
  });
}

function computeLabelLayouts(
  starts: { x: number; y: number }[],
  baseRadius: number,
): LabelLayout[] {
  const sameStartGroups = findSameStartGroups(starts);
  const groupedIndices = new Map<number, { members: number[]; position: number }>();

  for (const members of sameStartGroups) {
    const sorted = [...members].sort((a, b) => a - b);
    sorted.forEach((strokeIndex, position) => {
      groupedIndices.set(strokeIndex, { members: sorted, position });
    });
  }

  const initialLayouts = starts
    .map((pt, strokeIndex) => {
      if (!pt) return null;

      const group = groupedIndices.get(strokeIndex);
      if (!group) {
        const offset = getLabelOffsetFromStart(pt, baseRadius);
        return {
          strokeIndex,
          startX: pt.x,
          startY: pt.y,
          labelX: pt.x + offset.x,
          labelY: pt.y + offset.y,
          radius: baseRadius,
        };
      }

      const baseOffset = getLabelOffsetFromStart(pt, baseRadius);
      const fanSpread = baseRadius * 2.8;
      const fanOffset = getFanOffsetFromStart(
        group.position,
        group.members.length,
        pt,
        fanSpread,
      );

      return {
        strokeIndex,
        startX: pt.x,
        startY: pt.y,
        labelX: pt.x + baseOffset.x + fanOffset.x,
        labelY: pt.y + baseOffset.y + fanOffset.y,
        radius: group.position > 0 ? baseRadius * 0.88 : baseRadius,
      };
    })
    .filter((layout): layout is LabelLayout => layout !== null);

  return clampLabelLayouts(resolveLabelCollisions(initialLayouts, baseRadius));
}

function computeSequenceGroups(
  starts: { x: number; y: number }[],
  strokeCount: number,
): SequenceGroup[] {
  const sameStartGroups = findSameStartGroups(starts);

  const groups: SequenceGroup[] = [];
  let i = 0;
  while (i < strokeCount) {
    const sameGroup = sameStartGroups.find((members) => members.includes(i));
    if (sameGroup) {
      groups.push({
        strokeIndices: [...sameGroup].sort((a, b) => a - b),
      });
      i = Math.max(...sameGroup) + 1;
    } else {
      groups.push({ strokeIndices: [i] });
      i += 1;
    }
  }

  return groups;
}

function pointsToPath(points: { x: number; y: number }[]): string {
  if (points.length < 2) return '';
  let d = `M ${points[0].x.toFixed(2)} ${points[0].y.toFixed(2)}`;
  for (let i = 1; i < points.length; i++) {
    d += ` L ${points[i].x.toFixed(2)} ${points[i].y.toFixed(2)}`;
  }
  return d;
}

/**
 * KKJN-style: draw a short arc following the TAIL of the stroke (last 25-35%).
 * This shows the direction without covering the whole stroke with a parallel line.
 */
function computeArrowForStroke(el: SVGPathElement): ParallelArrow {
  const len = el.getTotalLength();
  if (len < MIN_ARROW_LENGTH) return { pathD: '' };

  // Use the last 25-35% of the stroke as the tail arrow segment
  const tailFraction = len < 25 ? 0.55 : len < 50 ? 0.38 : 0.28;
  const tStart = 1 - tailFraction;
  const sampleCount = Math.max(4, Math.ceil(len * tailFraction / 5));

  const points: { x: number; y: number }[] = [];
  for (let j = 0; j <= sampleCount; j++) {
    const t = tStart + (tailFraction * j) / sampleCount;
    const p = el.getPointAtLength(len * t);
    points.push({ x: p.x, y: p.y });
  }

  return { pathD: pointsToPath(points) };
}

function computeParallelArrows(refs: (SVGPathElement | null)[]): ParallelArrow[] {
  return refs.map((el) => {
    if (!el) return { pathD: '' };
    return computeArrowForStroke(el);
  });
}

/**
 * Renders a KKJN-style stroke-order guide for a kanji using KanjiVG data.
 * Black strokes; white-outlined red numbered circles; red direction arrows on
 * every stroke — horizontal strokes get arrows below, vertical strokes to the right.
 *
 * KanjiVG data © Ulrich Apel — CC BY-SA 3.0
 */
export const StrokeGuide: React.FC<Props> = ({ kanji, size = 96 }) => {
  const data = strokeOrderData[kanji];
  const pathRefs = useRef<(SVGPathElement | null)[]>([]);
  const [parallelArrows, setParallelArrows] = useState<ParallelArrow[]>([]);
  const arrowMarkerId = `stroke-arrow-${useId().replace(/:/g, '')}`;

  const layout = useMemo(() => {
    if (!data || data.paths.length === 0) return null;

    const strokeCount = data.paths.length;
    const radius = getCircleRadius(strokeCount);

    return {
      paths: data.paths,
      starts: data.starts,
      radius,
      fontSize: getFontSize(strokeCount),
      strokeCount,
      labelLayouts: computeLabelLayouts(data.starts, radius),
      sequenceGroups: computeSequenceGroups(data.starts, strokeCount),
    };
  }, [data]);

  useLayoutEffect(() => {
    if (!layout) {
      setParallelArrows([]);
      return;
    }

    pathRefs.current = pathRefs.current.slice(0, layout.paths.length);
    setParallelArrows(computeParallelArrows(pathRefs.current));
  }, [layout, kanji]);

  if (!layout) {
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
          background: '#fff',
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

  const { paths, fontSize, strokeCount, labelLayouts, sequenceGroups } = layout;
  const showSequence = strokeCount > 1;
  const listFontSize = Math.max(7, Math.min(9, size * 0.11));
  const sequenceWidth = Math.max(
    size,
    size * (strokeCount >= 10 ? 1.8 : strokeCount >= 7 ? 1.65 : 1.4),
  );
  const sequenceNoWrap = strokeCount <= 8;

  return (
    <div
      className="stroke-guide"
      title={`${kanji} の書き順`}
      style={{
        minWidth: size,
        maxWidth: showSequence ? sequenceWidth : size,
        flexShrink: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        background: '#fff',
        borderRadius: 4,
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
          <marker
            id={arrowMarkerId}
            viewBox="0 0 10 10"
            refX="9"
            refY="5"
            markerWidth="5"
            markerHeight="5"
            orient="auto"
            markerUnits="userSpaceOnUse"
          >
            <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill={ARROW_COLOR} />
          </marker>
        </defs>

        <rect
          x={0}
          y={0}
          width={KANJI_SIZE}
          height={KANJI_SIZE}
          fill="#fff"
          className="stroke-guide-bg"
        />

        {/* 1. All stroke paths — black */}
        {paths.map((d, i) => (
          <path
            key={`stroke-${i}`}
            ref={(el) => {
              pathRefs.current[i] = el;
            }}
            d={d}
            fill="none"
            stroke={STROKE_COLOR}
            strokeWidth={STROKE_WIDTH}
            strokeLinecap="round"
            strokeLinejoin="round"
            className="stroke-guide-base"
          />
        ))}

        {/* 2. KKJN-style tail arrows — red arc following the end of each stroke */}
        {parallelArrows.map((arrow, i) => {
          if (!arrow.pathD) return null;
          return (
            <path
              key={`arrow-${i}`}
              d={arrow.pathD}
              fill="none"
              stroke={ARROW_COLOR}
              strokeWidth={ARROW_STROKE_WIDTH}
              strokeLinecap="round"
              strokeLinejoin="round"
              markerEnd={`url(#${arrowMarkerId})`}
              className="stroke-guide-arrow"
            />
          );
        })}

        {/* 3. Numbered circles — white fill, red border, near stroke starts */}
        {labelLayouts.map((label) => (
          <g key={`num-${label.strokeIndex}`} className="stroke-guide-label">
            <circle
              cx={label.labelX}
              cy={label.labelY}
              r={label.radius}
              fill="#fff"
              stroke={ARROW_COLOR}
              strokeWidth={0.8}
            />
            <text
              x={label.labelX}
              y={label.labelY}
              textAnchor="middle"
              dominantBaseline="central"
              fontSize={fontSize}
              fontWeight="bold"
              fill={ARROW_COLOR}
              style={{ fontFamily: 'sans-serif', userSelect: 'none' }}
            >
              {label.strokeIndex + 1}
            </text>
          </g>
        ))}
      </svg>

      {showSequence && (
        <div
          className="stroke-guide-points"
          aria-label={`${kanji}の書き順`}
          style={{
            marginTop: 3,
            width: sequenceWidth,
            textAlign: 'center',
            userSelect: 'none',
          }}
        >
          <div
            className="stroke-guide-points-label"
            style={{
              fontSize: Math.max(6, listFontSize - 1),
              color: '#9ca3af',
              lineHeight: 1.2,
              marginBottom: 2,
            }}
          >
            かきじゅん
          </div>
          <div
            className="stroke-guide-sequence"
            style={{
              display: 'flex',
              flexWrap: sequenceNoWrap ? 'nowrap' : 'wrap',
              justifyContent: 'center',
              alignItems: 'center',
              gap: sequenceNoWrap ? '1px' : '2px 1px',
              fontSize: listFontSize,
              lineHeight: 1.3,
              color: ARROW_COLOR,
              letterSpacing: '0.02em',
            }}
          >
            {sequenceGroups.map((group, groupIndex) => (
              <React.Fragment key={`seq-group-${groupIndex}`}>
                {groupIndex > 0 && (
                  <span style={{ color: '#fca5a5', margin: '0 1px' }}>→</span>
                )}
                <span
                  className="stroke-guide-sequence-badge"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: 1,
                    minWidth: listFontSize + 2,
                    height: listFontSize + 2,
                    padding: group.strokeIndices.length > 1 ? '0 3px' : 0,
                    borderRadius: group.strokeIndices.length > 1 ? 6 : '50%',
                    background: '#fff',
                    border: `1px solid ${ARROW_COLOR}`,
                    color: ARROW_COLOR,
                    fontWeight: 700,
                    fontSize: listFontSize - 1,
                    verticalAlign: 'middle',
                  }}
                >
                  {group.strokeIndices.map((strokeIndex) => (
                    <span key={`seq-num-${strokeIndex}`}>{strokeIndex + 1}</span>
                  ))}
                </span>
              </React.Fragment>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
