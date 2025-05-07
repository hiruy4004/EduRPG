import { createClient } from '@supabase/supabase-js';

const supabaseUrl = "https://fcwnxnemszouhbunmkpv.supabase.co";
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZjd254bmVtc3pvdWhidW5ta3B2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY2NDY4MzYsImV4cCI6MjA2MjIyMjgzNn0.1_IeGzDSr_PQpYGit_tTgeMvKwcwUwgaQW2uGabXCGQ";

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Questions table operations
export async function getQuestionsByDifficulty(difficulty) {
  const { data, error } = await supabase
    .from('questions')
    .select('*')
    .eq('difficulty', difficulty);
  
  if (error) {
    console.error('Error fetching questions:', error);
    return [];
  }
  return data;
}

export async function addQuestion(question) {
  const { data, error } = await supabase
    .from('questions')
    .insert([question]);

  if (error) {
    console.error('Error adding question:', error);
    return null;
  }
  return data;
}