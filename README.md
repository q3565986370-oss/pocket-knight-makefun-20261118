# Pocket Knight

An original 4 KB Python chess-engine demonstration for tiny-chess-01.

- Full legal move generation, castling, en passant and all promotions.
- Deterministic iterative alpha-beta with bounded quiescence; 12,000-node budget, no search clock or randomness.
- Standard-library-only HTTP client: MAKEFUN_ENV_URL, /game and /move.

Verified locally with Python 3.14: start perft 20/400/8902/197281; Kiwipete 48/2039/97862; endgame 14/191/2812/43238; promotion-heavy reference depth 3 = 9467. Tests also covered pinned en passant, attacked castling transit, white/black promotions, mate in one, repeatability and mocked two-game protocol flow. Three sampled searches were roughly 0.8-2.0 seconds on the development machine, not a sandbox timing guarantee.

Target Python 3.13 has not been run. Official gauntlet/Elo and prize eligibility are unverified. Search has no repetition-history detection, transposition table or complete insufficient-material evaluator; the game service adjudicates final results. Public build evidence is a transparent manual handover, not native provider logs; no prize eligibility is claimed.
