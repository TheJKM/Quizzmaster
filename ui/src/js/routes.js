import HomePage from '../pages/home.f7.html';
import DashboardPage from '../pages/dashboard.f7.html';
import QuestionPage from '../pages/questions.f7.html';
import GradingPage from '../pages/grading.f7.html';
import TeamsPage from '../pages/teams.f7.html';
import AccountsPage from '../pages/accounts.f7.html';
import ScoreboardPage from '../pages/scoreboard.f7.html';
import InternalScoreboardPage from '../pages/scoreboardinternal.f7.html';
import SettingsPage from '../pages/settings.f7.html';

import NotFoundPage from '../pages/404.f7.html';

var routes = [
  {
    path: '/dashboard',
    component: DashboardPage,
  },
  {
    path: '/questions',
    component: QuestionPage,
  },
  {
    path: '/grading',
    component: GradingPage,
  },
  {
    path: '/teams',
    component: TeamsPage,
  },
  {
    path: '/accounts',
    component: AccountsPage,
  },
  {
    path: '/scoreboard',
    component: ScoreboardPage,
  },
  {
    path: '/scoreboardinternal',
    component: InternalScoreboardPage,
  },
  {
    path: '/settings',
    component: SettingsPage,
  },
  {
    path: '/:id?',
    component: HomePage,
  },
  {
    path: '(.*)',
    component: NotFoundPage,
  },
];

export default routes;
