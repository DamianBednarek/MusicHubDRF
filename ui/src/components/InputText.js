import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import React from "react";
function InputText(props) {
  return (
    <Grid item xs={12} sm={props.sm ? props.sm : 6}>
      <TextField
        name={props.name}
        required
        fullWidth
        id={props.name}
        label={props.label}
        value={props.value}
        onChange={(event) => {
          props.setValue(event.target.value);
        }}
        autoFocus
      />
    </Grid>
  );
}

export default InputText;
