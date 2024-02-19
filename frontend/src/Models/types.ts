export enum CellState {
    cross = "cross",
    ship = "ship",
    empty_shot = "empty_shot",
    fire = "fire",
    skull = "skull",
}

export type CellUpdate = {
    x: number;
    y: number;
    state: CellState;
}