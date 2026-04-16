import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Event: React.FC = () => {
  return (
    <div id="page-event-1">
    <div id="iab1i" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="iq1in" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="ihusg" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="inn6o" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="iddsz" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/calendar">{"Calendar"}</a>
          <a id="ij8jj" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/event">{"Event"}</a>
          <a id="iq4w3" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/category">{"Category"}</a>
        </div>
        <p id="ifyvo" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="ilx9t" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="i4j2f" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"Event"}</h1>
        <p id="idfds" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage Event data"}</p>
        <TableBlock id="table-event-1" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Event List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "/NumberEvents", "column_type": "field", "field": "/numberEvents", "type": "int", "required": true}, {"label": "Name", "column_type": "field", "field": "Name", "type": "str", "required": true}, {"label": "Date", "column_type": "field", "field": "Date", "type": "date", "required": true}, {"label": "Period", "column_type": "field", "field": "Period", "type": "timedelta", "required": true}], "formColumns": [{"column_type": "field", "field": "/numberEvents", "label": "/numberEvents", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "Name", "label": "Name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "Date", "label": "Date", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "Period", "label": "Period", "type": "timedelta", "required": true, "defaultValue": null}, {"column_type": "field", "field": "Place", "label": "Place", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "calendar", "field": "calendar", "lookup_field": "Name", "entity": "Calendar", "type": "str", "required": true}]}} dataBinding={{"entity": "Event", "endpoint": "/event/"}} />
      </main>
    </div>    </div>
  );
};

export default Event;
