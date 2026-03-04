import { TextField, Divider, Stack } from '@mui/material';

function Results() {
    return (
        <Stack spacing={4} sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>

            <TextField
                name='title'
                fullWidth
                label="Tytuł"
                variant="outlined"
                InputProps={{ sx: { borderRadius: 2 } }}
            />

            <TextField
                name='task'
                fullWidth
                label="Polecenie"
                multiline
                rows={6}
                variant="outlined"
                InputProps={{ sx: { borderRadius: 2 } }}
            />
            
            <TextField
                fullWidth
                multiline
                rows={6}
                label="Testy jednostkowe / Przypadki testowe"
                variant="outlined"
                InputProps={{ sx: { borderRadius: 2 } }}
            />

            <TextField
                fullWidth
                multiline
                rows={6}
                label="Wzorcowe rozwiązanie"
                variant="outlined"
                InputProps={{ sx: { borderRadius: 2 } }}
            />

        </Stack>
    );
}

export default Results;