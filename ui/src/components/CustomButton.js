import Button from "@mui/material/Button";
import React from "react";
function CustomButton(props) {
  return (
    <Button
      type="submit"
      fullWidth
      variant={props.variant ? props.variant : "contained"}
      sx={props.sx ? props.sx : { mt: 3, mb: 2 }}
      onClick={props.onClick}
    >
      {props.value}
    </Button>
  );
}

export default CustomButton;
