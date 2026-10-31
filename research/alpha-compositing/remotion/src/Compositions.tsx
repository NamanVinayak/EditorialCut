import React from "react";
import { AbsoluteFill } from "remotion";
import {
  Background,
  PresenterAlpha,
  RearText,
  FrontBadgeOverlay,
} from "./layers";

// 1. RearTypography: background (bottom) -> rear text -> presenter alpha (top)
// Text must be visibly occluded by the presenter.
export const RearTypography: React.FC = () => {
  return (
    <AbsoluteFill>
      <Background />
      <RearText />
      <PresenterAlpha />
    </AbsoluteFill>
  );
};

// 2. FrontBadge: background -> presenter alpha -> front badge (top, static)
// Badge always on top, never occluded.
export const FrontBadge: React.FC = () => {
  return (
    <AbsoluteFill>
      <Background />
      <PresenterAlpha />
      <FrontBadgeOverlay />
    </AbsoluteFill>
  );
};

// 3. Both: background -> rear text -> presenter alpha -> front badge (all 4 layers)
export const Both: React.FC = () => {
  return (
    <AbsoluteFill>
      <Background />
      <RearText />
      <PresenterAlpha />
      <FrontBadgeOverlay />
    </AbsoluteFill>
  );
};
