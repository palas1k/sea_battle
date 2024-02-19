import { makeAutoObservable } from "mobx";
import io, {Socket} from "socket.io-client";
import {CellState, CellUpdate} from "./types.ts";

class SeaBattleStore {
    grid: CellState[][] = Array(10)
        .fill(null)
        .map(() => Array(10).fill(CellState.cross));
    socket: Socket;

    constructor() {
        makeAutoObservable(this);
        this.socket = io("http://localhost:3001", { autoConnect: true });
        this.socket.on("cell-update", this.handleCellUpdate);
    }

    handleCellUpdate = ({ x, y, state }: CellUpdate) => {
        this.grid[x][y] = state;
    };

    tryHit(x: number, y: number): void {
        if (this.grid[x][y] === CellState.cross) {
            this.socket.emit("try-hit", { x, y, state: this.grid[x][y] });
        }
    }

    disconnect(): void {
        this.socket.disconnect();
    }
}

export default SeaBattleStore;