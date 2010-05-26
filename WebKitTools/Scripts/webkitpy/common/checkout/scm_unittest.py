from __future__ import with_statement

import codecs
# Callers could use run_and_throw_if_fail(args, cwd=cwd, quiet=True)
    # Note: Not thread safe: http://bugs.python.org/issue2320
def write_into_file_at_path(file_path, contents, encoding="utf-8"):
    with codecs.open(file_path, "w", encoding) as file:
        file.write(contents)


def read_from_path(file_path, encoding="utf-8"):
    with codecs.open(file_path, "r", encoding) as file:
        return file.read()


def _make_diff(command, *args):
    # We use this wrapper to disable output decoding. diffs should be treated as
    # binary files since they may include text files of multiple differnet encodings.
    return run_command([command, "diff"] + list(args), decode_output=False)


def _svn_diff(*args):
    return _make_diff("svn", *args)


def _git_diff(*args):
    return _make_diff("git", *args)

        # This 4th commit is used to make sure that our patch file handling
        # code correctly treats patches as binary and does not attempt to
        # decode them assuming they're utf-8.
        write_into_file_at_path("test_file", u"latin1 test: \u00A0\n", "latin1")
        write_into_file_at_path("test_file2", u"utf-8 test: \u00A0\n", "utf-8")
        # Create and checkout a trunk dir to match the standard svn configuration to match git-svn's expectations
        os.chdir(test_object.svn_checkout_path)
        os.mkdir('trunk')
        cls._svn_add('trunk')
        # We can add tags and branches as well if we ever need to test those.
        cls._svn_commit('add trunk')

        # Change directory out of the svn checkout so we can delete the checkout directory.
        # _setup_test_commits will CD back to the svn checkout directory.
        os.chdir('/')
        run_command(['rm', '-rf', test_object.svn_checkout_path])
        run_command(['svn', 'checkout', '--quiet', test_object.svn_repo_url + '/trunk', test_object.svn_checkout_path])

        # FIXME: This code is brittle if the Attachment API changes.
        attachment = Attachment({"bug_id": 12345}, None)
        attachment.contents = lambda: patch_contents
        attachment.reviewer = lambda: joe_cool
        changed_files = self.scm.changed_files_for_revision(3)
        self.assertEqual(sorted(self.scm.changed_files_for_revision(4)), sorted(["test_file", "test_file2"]))  # Git and SVN return different orders.
        self.assertEqual(self.scm.changed_files_for_revision(2), ["test_file"])
        self.assertEqual(self.scm.contents_at_revision("test_file", 3), "test1test2")
        self.assertEqual(self.scm.contents_at_revision("test_file", 4), "test1test2test3\n")

        # Verify that contents_at_revision returns a byte array, aka str():
        self.assertEqual(self.scm.contents_at_revision("test_file", 5), u"latin1 test: \u00A0\n".encode("latin1"))
        self.assertEqual(self.scm.contents_at_revision("test_file2", 5), u"utf-8 test: \u00A0\n".encode("utf-8"))
        self.assertEqual(self.scm.contents_at_revision("test_file2", 4), "second file")
        self.assertEqual(self.scm.committer_email_for_revision(3), getpass.getuser())  # Committer "email" will be the current user
        self.scm.apply_reverse_diff('5')
        r3_patch = self.scm.diff_for_revision(4)
        self.assertTrue(re.search('test2', self.scm.diff_for_revision(3)))
        added = read_from_path('fizzbuzz7.gif', encoding=None)
        modified = read_from_path('fizzbuzz7.gif', encoding=None)
    def test_detect_scm_system_relative_url(self):
        scm = detect_scm_system(".")
        # I wanted to assert that we got the right path, but there was some
        # crazy magic with temp folder names that I couldn't figure out.
        self.assertTrue(scm.checkout_root)

        actual_contents = read_from_path("test_file.swf", encoding=None)
        patch = self._create_patch(_svn_diff("-r5:4"))
        patch = self._create_patch(_svn_diff("-r3:5"))
        self.assertTrue(re.search('second commit', self.scm.svn_commit_log(3)))

    def _shared_test_commit_with_message(self, username=None):
        write_into_file_at_path('test_file', 'more test content')
        commit_text = self.scm.commit_with_message("another test commit", username)
        self.assertEqual(self.scm.svn_revision_from_commit_text(commit_text), '6')

        self.scm.dryrun = True
        write_into_file_at_path('test_file', 'still more test content')
        commit_text = self.scm.commit_with_message("yet another test commit", username)
        self.assertEqual(self.scm.svn_revision_from_commit_text(commit_text), '0')
        run_silent(['git', 'svn', 'clone', '-T', 'trunk', self.svn_repo_url, self.git_checkout_path])
        diff_to_common_base = _git_diff(self.scm.svn_branch_name() + '..')
        diff_to_merge_base = _git_diff(self.scm.svn_merge_base())
        patch = self._create_patch(_git_diff('HEAD..HEAD^'))
        patch = self._create_patch(_git_diff('HEAD~2..HEAD'))
        write_into_file_at_path('test_file', 'more test content')
        self.scm.commit_locally_with_message("another test commit")
        commit_text = self.scm.commit_with_message("another test commit")
        self.assertEqual(self.scm.svn_revision_from_commit_text(commit_text), '6')

        self.scm.dryrun = True
        write_into_file_at_path('test_file', 'still more test content')
        self.scm.commit_locally_with_message("yet another test commit")
        commit_text = self.scm.commit_with_message("yet another test commit")
        self.assertEqual(self.scm.svn_revision_from_commit_text(commit_text), '0')

    def _one_local_commit_plus_working_copy_changes(self):
        write_into_file_at_path('test_file_commit1', 'more test content')
        run_command(['git', 'add', 'test_file_commit1'])
        self.scm.commit_locally_with_message("another test commit")

        write_into_file_at_path('test_file_commit2', 'still more test content')
        run_command(['git', 'add', 'test_file_commit2'])

    def test_commit_with_message_working_copy_only(self):
        write_into_file_at_path('test_file_commit1', 'more test content')
        run_command(['git', 'add', 'test_file_commit1'])
        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("yet another test commit")

        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')
        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit1', svn_log))

    def test_commit_with_message_squashed(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("yet another test commit", squash=True)

        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')
        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit2', svn_log))
        self.assertTrue(re.search(r'test_file_commit1', svn_log))

    def _two_local_commits(self):
        write_into_file_at_path('test_file_commit1', 'more test content')
        run_command(['git', 'add', 'test_file_commit1'])
        self.scm.commit_locally_with_message("another test commit")

        write_into_file_at_path('test_file_commit2', 'still more test content')
        run_command(['git', 'add', 'test_file_commit2'])
        self.scm.commit_locally_with_message("yet another test commit")

    def test_commit_with_message_git_commit(self):
        self._two_local_commits()

        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("another test commit", git_commit="HEAD^")
        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')

        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit1', svn_log))
        self.assertFalse(re.search(r'test_file_commit2', svn_log))

    def test_commit_with_message_git_commit_range(self):
        self._two_local_commits()

        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("another test commit", git_commit="HEAD~2..HEAD")
        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')

        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit1', svn_log))
        self.assertTrue(re.search(r'test_file_commit2', svn_log))

    def test_commit_with_message_multiple_local_commits(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.commit_with_message, ["another test commit"])

    def test_commit_with_message_multiple_local_commits_and_working_copy(self):
        self._two_local_commits()
        write_into_file_at_path('test_file_commit1', 'working copy change')
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.commit_with_message, ["another test commit"])

    def test_commit_with_message_git_commit_and_working_copy(self):
        self._two_local_commits()
        write_into_file_at_path('test_file_commit1', 'working copy change')
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.commit_with_message, ["another test commit", 'git_commit="HEAD^"'])

    def test_commit_with_message_multiple_local_commits_no_squash(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("yet another test commit", squash=False)
        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')

        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit2', svn_log))
        self.assertFalse(re.search(r'test_file_commit1', svn_log))

        svn_log = run_command(['git', 'svn', 'log', '--limit=2', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit1', svn_log))

    def test_commit_with_message_multiple_local_commits_squash(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        commit_text = scm.commit_with_message("yet another test commit", squash=True)
        self.assertEqual(scm.svn_revision_from_commit_text(commit_text), '6')

        svn_log = run_command(['git', 'svn', 'log', '--limit=1', '--verbose'])
        self.assertTrue(re.search(r'test_file_commit2', svn_log))
        self.assertTrue(re.search(r'test_file_commit1', svn_log))

    def test_commit_with_message_not_synced_squash(self):
        run_command(['git', 'checkout', '-b', 'my-branch', 'trunk~3'])
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.commit_with_message, "another test commit", squash=True)
    def test_create_patch_local_plus_working_copy(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.create_patch)

    def test_create_patch_multiple_local_commits(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.create_patch)

    def test_create_patch_squashed(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch(squash=True)
        self.assertTrue(re.search(r'test_file_commit2', patch))
        self.assertTrue(re.search(r'test_file_commit1', patch))

    def test_create_patch_not_squashed(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch(squash=False)
        self.assertTrue(re.search(r'test_file_commit2', patch))
        self.assertFalse(re.search(r'test_file_commit1', patch))

    def test_create_patch_git_commit(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch(git_commit="HEAD^")
        self.assertTrue(re.search(r'test_file_commit1', patch))
        self.assertFalse(re.search(r'test_file_commit2', patch))

    def test_create_patch_git_commit_range(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch(git_commit="HEAD~2..HEAD")
        self.assertTrue(re.search(r'test_file_commit2', patch))
        self.assertTrue(re.search(r'test_file_commit1', patch))

    def test_create_patch_multiple_local_commits_no_squash(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch(squash=False)
        # FIXME: It's weird that with squash=False, create_patch/changed_files ignores local commits,
        # but commit_with_message commits them.
        self.assertTrue(patch == "")

    def test_create_patch_multiple_local_commits_squash(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        patch = scm.create_patch(squash=True)
        self.assertTrue(re.search(r'test_file_commit2', patch))
        self.assertTrue(re.search(r'test_file_commit1', patch))

    def test_create_patch_not_synced_squash(self):
        run_command(['git', 'checkout', '-b', 'my-branch', 'trunk~3'])
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.create_patch, squash=True)

        write_into_file_at_path(test_file_path, file_contents, encoding=None)
        self.assertEqual(file_contents, read_from_path(test_file_path, encoding=None))
        write_into_file_at_path(test_file_path, file_contents, encoding=None)
        patch_from_local_commit = scm.create_patch('HEAD')

    def test_changed_files_local_plus_working_copy(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.changed_files)

    def test_changed_files_multiple_local_commits(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.changed_files)

    def test_changed_files_squashed(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files(squash=True)
        self.assertTrue('test_file_commit2' in files)
        self.assertTrue('test_file_commit1' in files)

    def test_changed_files_not_squashed(self):
        self._one_local_commit_plus_working_copy_changes()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files(squash=False)
        self.assertTrue('test_file_commit2' in files)
        self.assertFalse('test_file_commit1' in files)

    def test_changed_files_git_commit(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files(git_commit="HEAD^")
        self.assertTrue('test_file_commit1' in files)
        self.assertFalse('test_file_commit2' in files)

    def test_changed_files_git_commit_range(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files(git_commit="HEAD~2..HEAD")
        self.assertTrue('test_file_commit1' in files)
        self.assertTrue('test_file_commit2' in files)

    def test_changed_files_multiple_local_commits_no_squash(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files(squash=False)
        # FIXME: It's weird that with squash=False, create_patch/changed_files ignores local commits,
        # but commit_with_message commits them.
        self.assertTrue(len(files) == 0)

    def test_changed_files_multiple_local_commits_squash(self):
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        files = scm.changed_files(squash=True)
        self.assertTrue('test_file_commit2' in files)
        self.assertTrue('test_file_commit1' in files)

    def test_changed_files_not_synced_squash(self):
        run_command(['git', 'checkout', '-b', 'my-branch', 'trunk~3'])
        self._two_local_commits()
        scm = detect_scm_system(self.git_checkout_path)
        self.assertRaises(ScriptError, scm.changed_files, squash=True)