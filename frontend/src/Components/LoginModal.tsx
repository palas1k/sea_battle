import {
    Container,
    CssBaseline,
    Box,
    Avatar,
    TextField,
    Typography,
    Button
} from "@mui/material";
import Modal from "@mui/material/Modal";
import {LockOutlined} from "@mui/icons-material";
import {useState} from "react";


interface LoginProps {
    open: boolean;
    handleSubmit: (login: string) => void;
    handleCancel: () => void;
}
export const LoginModal = ({handleSubmit, open, handleCancel}: LoginProps) => {
    const [login, setLogin] = useState<string>("");
    return (
        <Modal
            open={open}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Container maxWidth="xs" sx={{ background: "#EEE", minHeight: "30vh" }}>
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <LockOutlined />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Укажите имя
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="login"
                            label="Ваш логин"
                            name="login"
                            autoComplete="login"
                            autoFocus
                            onChange={e => setLogin(e.target.value)}
                        />
                        <Box flexDirection={"row"}>
                        <Button
                            type="button"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            onClick={() => handleSubmit(login)}
                        >
                            Установить имя
                        </Button>
                        <Button
                            type="button"
                            fullWidth
                            color="warning"
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            onClick={() => handleCancel()}
                        >
                            Отмена
                        </Button>
                        </Box>
                    </Box>
                </Box>
            </Container>
        </Modal>
    );
};