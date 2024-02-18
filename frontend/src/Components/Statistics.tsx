import {useStore} from "../Models/Root.ts";
import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Card,
    CardContent,
    Typography
} from "@mui/material";

export const Statistics = () => {
    const {user, opponent} = useStore();

    return (
        <Card sx={{ height: "50vh", width: "20vw", whiteSpace: 'nowrap', overflow: "auto"}}>
            <CardContent>
                <Typography variant="h5" component="div">Статистика игры</Typography>

                <Accordion defaultExpanded={true}>
                    <AccordionSummary>
                        <Typography>Ваше имя:</Typography> <Typography sx={{ ml: "10px"}}>{user.login}</Typography>

                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography>Однопалубники: 2</Typography>
                        <Typography >Двухпалубники: 1</Typography>
                    </AccordionDetails>
                </Accordion>
                <Accordion defaultExpanded={true}>
                    <AccordionSummary>
                        <Typography>Оппонент:</Typography> <Typography sx={{ ml: "10px"}}>{opponent?.login}</Typography>

                    </AccordionSummary>
                    <AccordionDetails>
                        <Typography>Однопалубники: 5</Typography>
                        <Typography >Двухпалубники: 3</Typography>
                    </AccordionDetails>
                </Accordion>
            </CardContent>

            <CardContent>
                <Accordion>
                    <AccordionSummary>
                        <Typography>История действий</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        Lorem ipsum dolor sit amet, consectet ut    enim
                    </AccordionDetails>
                </Accordion>
            </CardContent>
        </Card>
    );
};