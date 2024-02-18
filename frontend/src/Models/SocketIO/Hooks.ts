import {Socket, io} from "socket.io-client";
import {useRef} from "react";

interface useSocketIOProps<T> {
    host: string
    path: string
    compress?: boolean
    onMessage?: (message: T) => void
    onConnect?: () => void
    onDisconnect?: () => void
    onCustomCallbacks?: [string, (message?: any) => void][]
}

export const useSocketIO = <T>(props: useSocketIOProps<T>) => {
    const socket = useRef<Socket | null>(null);
    const socketIsRunningRef = useRef<boolean>(false);

    const start = () => {
        socket.current = io(props.host, {
            path: `${props.path}`,
            transports: ['websocket'],
        });

        socket.current.on('connect', () => {
            console.log(`Соединение ${props.path} открыто`);
            socketIsRunningRef.current = true;
            props.onConnect?.();
        });

        socket.current.on('disconnect', () => {
            console.log(`Соединение ${props.path} закрыто`);
            socketIsRunningRef.current = false;
            props.onDisconnect?.();
        });
        socket.current.on('close', () => {
            console.log(`Соединение ${props.path} закрыто`);
            socketIsRunningRef.current = false;
            props.onDisconnect?.();
        });

        socket.current.on('message', (message: T | null) => {
            if (!message || !props.onMessage) {
                return;
            }
            props.onMessage(message);
        });

        props.onCustomCallbacks?.forEach(customCallback => {
            if (!socket.current) {
                return;
            }
            socket.current.on(customCallback[0], (message?: any) => {
                customCallback[1](message);
            });
        });
    };

    const close = () => {
        socket.current?.disconnect();
    };

    return {
        socketIsRunning: socketIsRunningRef,
        current: socket.current,
        start,
        close
    };
};
