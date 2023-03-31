import Avatar from "@mui/material/Avatar";
import CssBaseline from "@mui/material/CssBaseline";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Link from "@mui/material/Link";
import Typography from "@mui/material/Typography";
import axios from "../Axios";
import CustomButton from "../components/CustomButton";
import GoogleSign from "../components/GoogleSign";
import Header from "../components/Header";
import InputText from "../components/InputText";
import { UseSnackbarQueue } from "../components/Snackbar";
export default function SignUp() {
  const navigate = useNavigate();
  const showSuccess = UseSnackbarQueue("success");
  const showError = UseSnackbarQueue("error");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastname] = useState("");
  const [password, setPassword] = useState("");
  const [confirmpassword, setConfrimPassword] = useState("");

  const handleSubmit = () => {
    const json = JSON.stringify({
      email,
      first_name: firstName,
      last_name: lastName,
      password,
      confirm_password: confirmpassword,
    });
    axios
      .post("user/signup/", json, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((res) => {
        showSuccess("Sucessfull aciton!");
        navigate("/");
      })
      .catch((err) => {
        showError(err.response.data.message);
      });
  };

  return (
    <>
      <Header />
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign up
          </Typography>
          <Box sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <InputText
                name="firstName"
                label="First Name"
                value={firstName}
                setValue={setFirstName}
              />
              <InputText
                name="lastName"
                label="Last Name"
                value={lastName}
                setValue={setLastname}
              />
              <InputText
                sm={12}
                name="email"
                label="Email Address"
                value={email}
                setValue={setEmail}
              />
              <InputText
                name="password"
                label="Password"
                value={password}
                setValue={setPassword}
              />
              <InputText
                name="confrimpassword"
                label="Confirm Password"
                value={confirmpassword}
                setValue={setConfrimPassword}
              />
            </Grid>
            <CustomButton onClick={handleSubmit} value="Sign Up" />

            <GoogleSign />
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="/login/" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </>
  );
}
