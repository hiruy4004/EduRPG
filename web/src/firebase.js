// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { collection, addDoc, getDocs } from "firebase/firestore";


// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAW46VWD_-9HYAwf4wMe_JvZ8Z1n-I3_fA",
  authDomain: "edurpg-f00ec.firebaseapp.com",
  databaseURL: "https://edurpg-f00ec-default-rtdb.firebaseio.com",
  projectId: "edurpg-f00ec",
  storageBucket: "edurpg-f00ec.firebasestorage.app",
  messagingSenderId: "783480475245",
  appId: "1:783480475245:web:4583ddc1f2bdee4e01b964",
  measurementId: "G-818B5F28ST"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Firebase Authentication
const auth = getAuth(app);
// Initialize Firestore
const db = getFirestore(app);

export { auth };
export { db };

// Firestore question management

// Add a question to Firestore
export async function addQuestion(question) {
  try {
    const docRef = await addDoc(collection(db, "questions"), question);
    return docRef.id;
  } catch (e) {
    console.error("Error adding question: ", e);
    return null;
  }
}

// Get all questions from Firestore
export async function getAllQuestions() {
  try {
    const querySnapshot = await getDocs(collection(db, "questions"));
    return querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  } catch (e) {
    console.error("Error fetching questions: ", e);
    return [];
  }
}
export default app;