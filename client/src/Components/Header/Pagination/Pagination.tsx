import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';

export default function StyledPagination({currentPage, totalPages, loading, onPageChange}: {
    currentPage: number;
    totalPages: number;
    loading: boolean;
    onPageChange: (newPage: number) => void;
}) {
    return (
        <Stack spacing={2} direction="row" alignItems="center" justifyContent="center" padding="50px">
            <Pagination
                count={totalPages}
                variant="outlined"
                color="primary"
                page={currentPage}
                onChange={(_, page) => onPageChange(page)}
                disabled={loading}
                sx={{'& button, & .MuiPaginationItem-page': {color: 'white'}}}
            />
        </Stack>
    );
}