import {makeAutoObservable} from "mobx";

export class UserStore {
    nickname = '';

    constructor() {
        makeAutoObservable(this);
    }

    setNickname(nickname: string) {
        this.nickname = nickname;
    }
}