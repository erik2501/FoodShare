import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import FormControlLabel from "@material-ui/core/FormControlLabel";

const HomePageDisplay = () => {
  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component="h2" variant="h2" id="title">
          Welcome to FoodShare
        </Typography>
        <Button
          color="primary"
          variant="contained"
          to="recipe"
          component={Link}
        >
          Create recipe
        </Button>
      </Grid>
    </Grid>
  );
};

export default HomePageDisplay;