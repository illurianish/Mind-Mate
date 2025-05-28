const config = {
  apiUrl: process.env.NODE_ENV === 'production'
    ? 'https://mindmate-backend-f35c.onrender.com'  // Production Render.com URL
    : 'http://localhost:5002'  // Development backend URL
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