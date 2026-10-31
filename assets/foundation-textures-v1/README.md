# Foundation Texture Pack v1

A small, reusable foundation pack for the editing agent's unified design pass.
These are production ingredients, not copied graphics from the 24 reference
videos and not a permanent keyword-to-stock library.

The table below covers mechanics (blend modes and opacity bands). The judgment
layer — when texture serves the story and when it must be rejected — lives in
[`docs/rulebook/texture-language.md`](../../docs/rulebook/texture-language.md).

## Not included in this repository: download these yourself

Six Pixabay files are used by the pack but are not committed here, because the
Pixabay Content License does not allow redistributing the raw files. Download
each one (free, no attribution required) and save it at the path shown. The
two preview contact sheets built from them (`previews/motion-contact-sheet.jpg`,
`previews/paper-fabric-contact-sheet.jpg`) are also left out.

| Save as | Pixabay ID | Link |
| --- | --- | --- |
| `motion/grain/film-grain-loop-4k-30fps.mp4` | video 265935 | <https://pixabay.com/videos/id-265935/> |
| `motion/dust-scratches/old-film-dust-scratches-1080p-25fps.mp4` | video 245078 | <https://pixabay.com/videos/id-245078/> |
| `motion/flicker/old-film-flicker-overlay-4k-23.976fps.mp4` | video 39072 | <https://pixabay.com/videos/id-39072/> |
| `motion/light-leaks/film-burn-light-leak-4k-60fps.mp4` | video 211191 | <https://pixabay.com/videos/id-211191/> |
| `motion/light-leaks/film-scratch-light-leak-1080p-29fps.mp4` | video 282103 | <https://pixabay.com/videos/id-282103/> |
| `paper/torn-paper-edge-transparent-1920.png` | image 1816679 | search the ID on <https://pixabay.com> |

Everything else in the pack (ambientCG and Openclipart) is CC0 and included.
`checksums.sha256` still lists the files above so you can verify your downloads.

## What is included

- **Paper:** subtle white fiber, crumpled white paper, warm ribbed paper, a
  transparent torn notebook-paper plate, and grayscale height mattes.
- **Fabric:** neutral grey cloth and rough neutral textile, each with a
  grayscale height matte.
- **Ink and distress:** two resolution-independent ink vectors plus seamless
  granular-stain and scratch/reveal mattes.
- **Motion:** film grain, dust/scratches, restrained old-film flicker, an amber
  film burn, and a saturated pink/red film-scratch leak.

The pack contains **20 production files** plus three lightweight contact-sheet
previews. Total size is approximately **111 MB**.

## Editing use

| Family | Default treatment | Good for | Avoid |
| --- | --- | --- | --- |
| Paper/fabric colour plates | Normal, Multiply, or Soft Light at roughly 10–35% | Paper-cutout worlds, tactile backgrounds, subtle type texture | Full-strength texture over faces |
| Height/reveal mattes | Luma/alpha matte, displacement input, or contrast source | Rough reveals, edge breakup, print wear, ink absorption | Treating them as visible final artwork |
| Ink SVGs | Use directly as vector art or as alpha/luma masks | Ink wipes, distressed frames, controlled splatter accents | Repeating the same splat in every scene |
| White-background grain | Multiply/Darken, generally 5–20% | Gentle paper/film life | Screen mode; it will wash out the picture |
| Black-background dust/scratches | Screen/Add, generally 5–25% | Vintage accents and brief texture beats | Running it continuously at high opacity |
| Grey old-film flicker | Overlay/Soft Light or use its luma as an exposure driver | Subtle exposure instability | Strong flicker near accessibility-sensitive passages |
| Light leaks/film burns | Screen/Add, generally 10–40% | Sparse transitions, emotional accents | Using them as constant wallpaper |

These percentages are starting points, not fixed rules. The creative director
should choose intensity from the scene and protect presenter skin, legibility,
and visual hierarchy.

## Tiling and looping truth

- Files named `seamless` come from seamless ambientCG materials and can tile.
- `film-grain-loop-4k-30fps.mp4` is source-described as a loop.
- The remaining motion files are useful overlay **plates**, but a perfectly
  invisible end-to-start loop has not been claimed. Trim, offset, reverse, or
  crossfade them when a shot outlasts the source.
- The torn-paper PNG and ink SVGs do not tile.

## Licensing boundary

- ambientCG materials and the Openclipart ink vectors are CC0/public-domain
  foundations and may be modified and reused commercially.
- Pixabay files may be used and modified in finished creative work, but must
  not be redistributed as standalone stock. Keep those raw files inside this
  local production workspace.

See [MANIFEST.md](./MANIFEST.md) and [licenses/README.md](./licenses/README.md)
for per-source provenance and restrictions.
`checksums.sha256` provides an integrity check for every production file.

## Previews

- `previews/paper-fabric-contact-sheet.jpg`
- `previews/ink-contact-sheet.jpg`
- `previews/motion-contact-sheet.jpg`
