import os
from dataclasses import dataclass

from git import Repo

from mobt.GitCli.GitPython import log_undoing_all_git_commands
from mobt.GitCli.GitPython.GitActions.GitAction import GitAction


@dataclass()
class PullWithRebase(GitAction):
    repo: Repo

    def __post_init__(self):
        super().__post_init__()
        self._original_sha = None

    def _execute(self) -> None:
        tracking_branch = self.repo.active_branch.tracking_branch()
        if not tracking_branch:
            return

        remote_sha = tracking_branch.commit.hexsha
        self._original_sha = self.repo.active_branch.commit.hexsha

        if self._original_sha == remote_sha:
            return

        try:
            self.repo.git.pull('--rebase')
        except Exception as e:
            log_undoing_all_git_commands()
            self._undo()
            raise e

    def _undo(self):
        if not self._original_sha:
            return

        git_dir = self.repo.git_dir
        rebase_merge_exists = os.path.exists(os.path.join(git_dir, 'rebase-merge'))
        if rebase_merge_exists or os.path.exists(os.path.join(git_dir, 'rebase-apply')):
            self.repo.git.rebase('--abort')

        self.repo.git.reset("--hard", self._original_sha)
