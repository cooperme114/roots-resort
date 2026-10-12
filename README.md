# Roots Resort

A Greek and Latin roots theme park game.

## Attractions

### Carousel

The approved carousel prototype includes the detailed base, canopy, center column, 12 horse-angle sprites, guests boarding and unloading, rider heads, pause/2x speed, and the front-right lift adjustment.

**Important:** The working carousel prototype is not yet committed to this repository. Preserve `carousel_demo_front_right_lift.html` as the approved reference before refactoring it into a reusable attraction.

Planned structure:

- `attractions/carousel/` — reusable carousel module and its art assets
- `demo/` — standalone attraction testing
- `index.html` — eventual Roots Resort game

The original standalone HTML demo contains embedded sprite images; keep it intact until the reusable module is verified.
