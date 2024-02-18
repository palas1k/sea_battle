import {DataGrid, GridCellParams, GridColDef} from '@mui/x-data-grid';
import {useMemo} from "react";

const columns: GridColDef[] = Array.from(Array(6)).map(
    (_, index) => ({
        field: (index).toString(),
        headerName: index != 0 ? (index - 1).toString() : "",
        editable: false,
        type: "singleSelect",
        sortable: false,
        resizable: false,
        disableColumnMenu: true,
        filterable: false,
        align: "center",
        headerAlign: "center",
        groupable: false,
        width: 75,
    })
)

interface FieldProps {
    owner: any;
    editable: boolean;
    clickHandler?: (a: number, b: number) => void;
}

export const Field = ({owner, editable, clickHandler}: FieldProps) => {

    const handleClick = (e: GridCellParams) => clickHandler && editable && e.field != "0" && clickHandler(parseInt((e.id).toString()), parseInt(e.field) - 1);
    const rows = useMemo(() =>{
        console.log(owner.getFields());

        return owner !== null ? owner.getFields() :
        (Array.from(Array(5)).map(
        (_, index) => ({
            id: index.toString(),
            "0": index,
            "1": ".",
            "2": ".",
            "3": ".",
            "4": ".",
        })))
    }, []);
    return (
        <>
            <DataGrid onCellClick={e => handleClick(e)} columns={columns} rows={rows} disableColumnFilter disableRowSelectionOnClick hideFooterPagination disableColumnMenu disableDensitySelector disableColumnSelector scrollbarSize={0} density={"comfortable"}/>
        </>
    )
};