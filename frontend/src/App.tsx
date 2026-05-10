import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import LandingPage from "./pages/LandingPage";
import ConsentPage from "./pages/ConsentPage";
import ChatPage from "./pages/ChatPage";
import SurveyPage from "./pages/SurveyPage";
import CompletePage from "./pages/CompletePage";
import NotFoundPage from "./pages/NotFoundPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/:token" element={<LandingPage />} />
        <Route path="/:token/consent" element={<ConsentPage />} />
        <Route path="/:token/chat" element={<ChatPage />} />
        <Route path="/:token/survey" element={<SurveyPage />} />
        <Route path="/:token/complete" element={<CompletePage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Layout>
  );
}
