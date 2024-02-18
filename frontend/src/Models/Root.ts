import {Instance, onSnapshot, types} from "mobx-state-tree";
import {createContext, useContext} from "react";
import {Containment} from "./types.tsx";


export const Cell = types.model({
    x: types.integer,
    y: types.integer,
    containment: types.optional(types.string, Containment.cross.toString()),
});
export const Field = types.model({
    cells: types.array(types.array(Cell))
});
export const User = types.model({
    login: types.maybeNull(types.string),
    field: types.maybeNull(Field)
}).actions((self => ({
    setLogin(login: string) {
        self.login = login
    }
}))).views((self => ({
    authenticated() {
        return self.login === null;
    },
    getFields() {
        return (self.field?.cells.map( col => ({
            "id": col[0],
            "0": col[0],
            "1": col[1],
            "2": col[2],
            "3": col[3],
            "4": col[4],
        })))
    }
})))

const generateCells = () => Array.from(Array(5)).map(
    (_, column) => Array.from(Array(5)).map(
        (_, row) => ({
            x: row, y: column, containment: Containment.cross
        })
    )
)

export const RootModel = types.model({
    turn: types.boolean,
    user: User,
    opponent: types.maybeNull(User)
});

let initialState = RootModel.create({
    turn: false,
    user: { login: null, field: {cells:  generateCells()}},
    opponent: { login: "Jopa", field: { cells: generateCells()}}
});

const data = localStorage.getItem("rootState");
if (data) {
    const json = JSON.parse(data);
    if (RootModel.is(json)) {
        initialState = RootModel.create(json);
    }
}

export const rootStore = initialState;

onSnapshot(rootStore, (snapshot) => {
    console.log("Snapshot: ", snapshot);
    localStorage.setItem("rootState", JSON.stringify(snapshot));
});

export type UserInstance = Instance<typeof User>;

export type RootInstance = Instance<typeof RootModel>;
const RootStoreContext = createContext<null | RootInstance>(null);

export const StoreProvider = RootStoreContext.Provider;
export function useStore() {
    const store = useContext(RootStoreContext);
    if (store === null) {
        throw new Error("Store cannot be null, please add a context provider");
    }
    return store;
}