const config = {
  apiUrl: process.env.REACT_APP_API_URL || 
    (process.env.NODE_ENV === 'production'
      ? 'https://mind-mate-fe88.onrender.com'
      : 'http://localhost:5002'),
  
  // Add timeout for API calls
  apiTimeout: 30000, // 30 seconds
  
  // Add retry configuration
  maxRetries: 3,
  retryDelay: 1000, // 1 second
};

export default config;

export const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID || '';

// Mood tracking constants
export const MOOD_LEVELS = [1, 2, 3, 4, 5];
export const ENERGY_LEVELS = [1, 2, 3, 4, 5];
export const ANXIETY_LEVELS = [1, 2, 3, 4, 5];

// Activities for mood tracking
export const ACTIVITIES = [
    'Exercise',
    'Meditation',
    'Reading',
    'Social Activity',
    'Work',
    'Hobbies',
    'Rest',
    'Other'
];

// CBT Exercise Types
export const CBT_EXERCISE_TYPES = [
    'Thought Record',
    'Behavioral Activation',
    'Exposure Hierarchy',
    'Problem Solving',
    'Relaxation'
]; 