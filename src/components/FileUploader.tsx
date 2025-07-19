import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import {
  Box,
  Typography,
  Button,
  CircularProgress,
  styled,
} from '@mui/material'
import { CloudUpload, Description } from '@mui/icons-material'

const DropZone = styled(Box)(({ theme }) => ({
  border: `2px dashed rgba(255, 255, 255, 0.5)`,
  borderRadius: theme.spacing(2),
  padding: theme.spacing(4),
  textAlign: 'center',
  cursor: 'pointer',
  transition: 'all 0.3s ease',
  backgroundColor: 'rgba(255, 255, 255, 0.1)',
  '&:hover': {
    borderColor: 'rgba(255, 255, 255, 0.8)',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
  },
  '&.dragActive': {
    borderColor: 'rgba(255, 255, 255, 1)',
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
  },
}))

interface FileUploaderProps {
  onFileUpload: (file: File) => void
  isLoading: boolean
}

const FileUploader: React.FC<FileUploaderProps> = ({ onFileUpload, isLoading }) => {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFileUpload(acceptedFiles[0])
      }
    },
    [onFileUpload]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/octet-stream': ['.qvd'],
    },
    multiple: false,
  })

  if (isLoading) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" gap={2}>
        <CircularProgress color="inherit" />
        <Typography variant="body2">
          Procesando archivo QVD...
        </Typography>
      </Box>
    )
  }

  return (
    <DropZone
      {...getRootProps()}
      className={isDragActive ? 'dragActive' : ''}
    >
      <input {...getInputProps()} />
      <CloudUpload sx={{ fontSize: 48, mb: 2, opacity: 0.8 }} />
      {isDragActive ? (
        <Typography variant="body1" gutterBottom>
          Suelta el archivo QVD aquí...
        </Typography>
      ) : (
        <>
          <Typography variant="body1" gutterBottom>
            Arrastra y suelta un archivo QVD aquí
          </Typography>
          <Typography variant="body2" sx={{ mb: 2, opacity: 0.8 }}>
            o
          </Typography>
          <Button
            variant="outlined"
            color="inherit"
            startIcon={<Description />}
            sx={{
              borderColor: 'rgba(255, 255, 255, 0.5)',
              color: 'white',
              '&:hover': {
                borderColor: 'white',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
          >
            Seleccionar Archivo
          </Button>
        </>
      )}
      <Typography variant="caption" display="block" sx={{ mt: 2, opacity: 0.7 }}>
        Solo archivos .qvd son aceptados
      </Typography>
    </DropZone>
  )
}

export default FileUploader