import { makeAutoObservable } from 'mobx';
import { observer } from 'mobx-react-lite';
import { UserStore } from './User';
import { SeaBattleStore } from './SeaBattle';

class GameStore {
    opponentNickname = '';
    currentTurn = '';
    userBattlefield = new SeaBattleStore();
    opponentBattlefield = new SeaBattleStore();

    constructor(userStore: UserStore) {
        makeAutoObservable(this);
        this.currentTurn = userStore.nickname;
    }

    setOpponentNickname(nickname: string) {
        this.opponentNickname = nickname;
    }

    setCurrentTurn(nickname: string) {
        this.currentTurn = nickname;
    }

    setUserBattlefield(battlefield: SeaBattleStore) {
        this.userBattlefield = battlefield;
    }

    setOpponentBattlefield(battlefield: SeaBattleStore) {
        this.opponentBattlefield = battlefield;
    }
}

const gameStore = new GameStore(userStore);

const GameStoreProvider: React.FC = ({ children }) => {
    return (
        <GameStoreContext.Provider value={gameStore}>
            {children}
            </GameStoreContext.Provider>
    );
};

const GameStoreConsumer = observer(({ children }) => {
    const gameStore = useContext(GameStoreContext);

    return children(gameStore);
});

export { gameStore, GameStoreProvider, GameStoreConsumer };

const GameStoreContext = createContext(gameStore);