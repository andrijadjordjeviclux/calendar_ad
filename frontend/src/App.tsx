import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Calendar from "./pages/Calendar";
import Event from "./pages/Event";
import Category from "./pages/Category";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/calendar" element={<Calendar />} />
            <Route path="/event" element={<Event />} />
            <Route path="/category" element={<Category />} />
            <Route path="/" element={<Navigate to="/calendar" replace />} />
            <Route path="*" element={<Navigate to="/calendar" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
