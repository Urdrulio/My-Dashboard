import React from 'react'
import {
  FormControl,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Button,
  Box,
  Typography,
  Chip,
} from '@mui/material'
import { SelectAll, Deselect } from '@mui/icons-material'

interface ColumnSelectorProps {
  columns: string[]
  selectedColumns: string[]
  onSelectionChange: (selectedColumns: string[]) => void
}

const ColumnSelector: React.FC<ColumnSelectorProps> = ({
  columns,
  selectedColumns,
  onSelectionChange,
}) => {
  const handleColumnToggle = (column: string) => {
    const newSelection = selectedColumns.includes(column)
      ? selectedColumns.filter(col => col !== column)
      : [...selectedColumns, column]
    
    onSelectionChange(newSelection)
  }

  const handleSelectAll = () => {
    onSelectionChange(columns)
  }

  const handleDeselectAll = () => {
    onSelectionChange([])
  }

  return (
    <Box>
      <Box display="flex" gap={1} mb={2}>
        <Button
          size="small"
          variant="outlined"
          startIcon={<SelectAll />}
          onClick={handleSelectAll}
          disabled={selectedColumns.length === columns.length}
        >
          Todo
        </Button>
        <Button
          size="small"
          variant="outlined"
          startIcon={<Deselect />}
          onClick={handleDeselectAll}
          disabled={selectedColumns.length === 0}
        >
          Nada
        </Button>
      </Box>

      <Typography variant="body2" color="text.secondary" gutterBottom>
        Seleccionadas: <Chip label={selectedColumns.length} size="small" color="primary" /> de {columns.length}
      </Typography>

      <FormControl component="fieldset" variant="standard">
        <FormGroup>
          {columns.map((column) => (
            <FormControlLabel
              key={column}
              control={
                <Checkbox
                  checked={selectedColumns.includes(column)}
                  onChange={() => handleColumnToggle(column)}
                  size="small"
                />
              }
              label={
                <Typography variant="body2" noWrap title={column}>
                  {column}
                </Typography>
              }
              sx={{ 
                '& .MuiFormControlLabel-label': { 
                  maxWidth: '200px',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }
              }}
            />
          ))}
        </FormGroup>
      </FormControl>
    </Box>
  )
}

export default ColumnSelector