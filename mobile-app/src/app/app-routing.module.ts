import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: '', loadChildren: './tabs/tabs.module#TabsPageModule' },
  { path: 'list', loadChildren: './pages/events/list/list.module#ListPageModule' },
  { path: 'details/:myid', loadChildren: './pages/events/event-details/event-details.module#EventDetailsPageModule' },
  { path: 'update/:id', loadChildren: './pages/events/update/update.module#UpdatePageModule' }
];
@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
