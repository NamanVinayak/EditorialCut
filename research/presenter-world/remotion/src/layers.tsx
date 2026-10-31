import React from "react";
import { AbsoluteFill, staticFile } from "remotion";
import { Video } from "@remotion/media";

// Neutral diagnostic layers for the alpha-compositing benchmark.
// Grays only (#888/#999 range), plain sans-serif, no animation, no color
// accents, no drop shadows. These are evidence surfaces, not designs.

export const Background: React.FC = () => {
  return (
    <AbsoluteFill>
      <Video
        src={staticFile("background-270-290.mp4")}
        style={{ width: "100%", height: "100%" }}
        objectFit="cover"
        muted
      />
    </AbsoluteFill>
  );
};

export const PresenterAlpha: React.FC = () => {
  return (
    <AbsoluteFill>
      <Video
        src={staticFile("cutout-alpha.mov")}
        style={{ width: "100%", height: "100%" }}
        objectFit="cover"
        muted
      />
    </AbsoluteFill>
  );
};

export const RearText: React.FC = () => {
  // Positioned so the text block spans roughly the top 40% of the frame
  // height, where the presenter's head/shoulders sit in the source footage
  // (verified against a sample frame of the alpha cutout), so the presenter
  // clearly overlaps/occludes the text.
  return (
    <div
      style={{
        position: "absolute",
        top: "8%",
        left: 0,
        width: "100%",
        height: "40%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          fontFamily: "Arial, Helvetica, sans-serif",
          fontWeight: 700,
          fontSize: 180,
          lineHeight: 1,
          color: "#999999",
          textAlign: "center",
          whiteSpace: "nowrap",
        }}
      >
        REAR LAYER TEST
      </div>
    </div>
  );
};

export const FrontBadgeOverlay: React.FC = () => {
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          top: 60,
          left: 60,
          width: 300,
          height: 100,
          borderRadius: 16,
          backgroundColor: "#888888",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <span
          style={{
            fontFamily: "Arial, Helvetica, sans-serif",
            fontWeight: 700,
            fontSize: 40,
            color: "#333333",
          }}
        >
          FRONT
        </span>
      </div>
    </AbsoluteFill>
  );
};
