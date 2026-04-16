import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Calendar: React.FC = () => {
  return (
    <div id="page-calendar-0">
    <div id="i04xg" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="irel4" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="igb1c" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ix4e6" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="ijafe" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/calendar">{"Calendar"}</a>
          <a id="ixw2j" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/event">{"Event"}</a>
          <a id="i7ips" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/category">{"Category"}</a>
        </div>
        <p id="iztgj" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="ihn2f" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="idhxl" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"Calendar"}</h1>
        <p id="irvr6" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage Calendar data"}</p>
        <TableBlock id="table-calendar-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Calendar List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Name", "column_type": "field", "field": "Name", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "Name", "label": "Name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "event", "field": "event", "lookup_field": "/numberEvents", "entity": "Event", "type": "list", "required": false}]}} dataBinding={{"entity": "Calendar", "endpoint": "/calendar/"}} />
      </main>
    </div>    </div>
  );
};

export default Calendar;
