import React, { useState, useRef, useEffect } from 'react';
import { 
  Container, 
  Paper, 
  TextField, 
  Button, 
  Box,
  Typography,
  CircularProgress,
  IconButton,
  useTheme
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import SchoolIcon from '@mui/icons-material/School';
import axios from 'axios';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const theme = useTheme();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = {
      type: 'user',
      content: input
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/query', {
        prompt: input
      });

      if (response.data.metadata) {
        const matchMessage = {
          type: 'bot',
          content: `Found matching course: ${response.data.metadata}`,
        };
        setMessages(prev => [...prev, matchMessage]);
      }

      const botMessage = {
        type: 'bot',
        content: response.data.refined_response || 'Sorry, I could not find any relevant information.',
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        type: 'bot',
        content: 'Sorry, I encountered an error. Please try again.',
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setIsLoading(false);
  };

  return (
    <Box sx={{ 
      minHeight: '100vh',
      background: 'linear-gradient(145deg, #f0f9ff 0%, #e0f2fe 100%)',
      py: 4
    }}>
      <Container maxWidth="md">
        <Paper 
          elevation={2} 
          sx={{ 
            height: '85vh',
            display: 'flex', 
            flexDirection: 'column',
            overflow: 'hidden',
            border: '1px solid',
            borderColor: 'grey.200',
          }}
        >
          <Box sx={{ 
            p: 2.5, 
            borderBottom: 1, 
            borderColor: 'grey.200',
            background: 'white',
            display: 'flex',
            alignItems: 'center',
            gap: 2
          }}>
            <SchoolIcon color="primary" sx={{ fontSize: 28 }} />
            <Typography variant="h4" color="primary.dark">
              Course Query Assistant
            </Typography>
          </Box>
          
          <Box sx={{ 
            flexGrow: 1, 
            overflow: 'auto', 
            p: 3,
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
            bgcolor: 'background.default'
          }}>
            {messages.map((message, index) => (
              <Box
                key={index}
                sx={{
                  alignSelf: message.type === 'user' ? 'flex-end' : 'flex-start',
                  maxWidth: '75%',
                  animation: 'fadeIn 0.3s ease-in',
                  '@keyframes fadeIn': {
                    '0%': {
                      opacity: 0,
                      transform: 'translateY(10px)'
                    },
                    '100%': {
                      opacity: 1,
                      transform: 'translateY(0)'
                    },
                  },
                }}
              >
                <Paper
                  elevation={0}
                  sx={{
                    p: 2,
                    borderRadius: message.type === 'user' ? '20px 20px 5px 20px' : '20px 20px 20px 5px',
                    backgroundColor: message.type === 'user' 
                      ? 'primary.main' 
                      : 'white',
                    color: message.type === 'user' ? 'white' : 'text.primary',
                    border: message.type === 'bot' ? 1 : 0,
                    borderColor: 'grey.200',
                    boxShadow: message.type === 'bot' 
                      ? '0 2px 4px rgba(0,0,0,0.05)' 
                      : '0 2px 4px rgba(0,0,0,0.1)',
                  }}
                >
                  <Typography sx={{ whiteSpace: 'pre-wrap' }}>
                    {message.content}
                  </Typography>
                  {message.metadata && (
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        mt: 1,
                        color: message.type === 'user' ? 'grey.100' : 'text.secondary',
                        fontStyle: 'italic'
                      }}
                    >
                      {message.metadata}
                    </Typography>
                  )}
                </Paper>
              </Box>
            ))}
            {isLoading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
                <CircularProgress size={30} />
              </Box>
            )}
            <div ref={messagesEndRef} />
          </Box>

          <Box 
            component="form" 
            onSubmit={handleSubmit} 
            sx={{ 
              p: 2,
              borderTop: 1,
              borderColor: 'grey.200',
              bgcolor: 'white'
            }}
          >
            <Box sx={{ display: 'flex', gap: 1 }}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder="Ask about a course..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={isLoading}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    backgroundColor: 'grey.50'
                  }
                }}
              />
              <IconButton 
                color="primary"
                type="submit"
                disabled={isLoading || !input.trim()}
                sx={{ 
                  p: '10px',
                  bgcolor: 'primary.main',
                  color: 'white',
                  '&:hover': {
                    bgcolor: 'primary.dark',
                  },
                  '&.Mui-disabled': {
                    bgcolor: 'grey.300',
                    color: 'grey.500'
                  }
                }}
              >
                <SendIcon />
              </IconButton>
            </Box>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}

export default App; 