import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.html',
  styleUrls: ['./home.scss']
})
export class Home{
  constructor(private router: Router) {}

  goToAddRecipe() {
    this.router.navigate(['add-recipe']);
  }

  goToViewRecipes() {
    this.router.navigate(['view-recipe']);
  }

  goToFavorites() {
    this.router.navigate(['favorite-recipes']);
  }
}
