import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import * as React from "react";
export default function ButtonAppBar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" style={{ background: "#1B1B3A" }}>
        <Toolbar>
          <Typography
            variant="h6"
            component="a"
            href="/"
            sx={{ flexGrow: 1, color: "#E8F7EE", textDecoration: "none" }}
          >
            MusicHub
          </Typography>

          <Button href="/login/" color="inherit">
            Login
          </Button>

          <Button href="/register/" color="inherit">
            Register
          </Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
