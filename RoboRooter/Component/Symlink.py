

import FileHint
import os
import logging


class Symlink(FileHint.FileHint):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.hint_name = './manifests/symlinks'
        self.state_expression = r'^(.+)\s+(.+)$'
        self.rules = []

    def _filter_violations(self, path):
        for rule in self.rules:
            self.logger.debug(
                'Testing rule: %s',
                rule
            )
            link_src = self._relativize_link(rule[0], rule[1])
            link_dest = os.path.join(path, rule[1])

            if not self._is_path_linking_to_location(link_src, link_dest):
                self.logger.info(
                    'Expected %s to link to %s',
                    link_dest,
                    link_src
                )
                yield (link_src, link_dest)

    def _relativize_link(self, source, target):
            src_dir = os.path.normpath(os.path.dirname(source))
            src_file = os.path.normpath(os.path.basename(source))
            target_dir = os.path.dirname(target)

            relative_location = os.path.relpath(src_dir, target_dir)

            link_src = os.path.join(relative_location, src_file)

            return link_src

    def _is_path_linking_to_location(self, source, target):
        if not os.path.exists(target):
            return False

        if not os.path.islink(target):
            return False

        if os.path.normpath(os.readlink(target)) != os.path.normpath(source):
            return False

        return True

    def fix(self, path):
        for change in self._filter_violations(path):
            self.logger.info(
                'Creating symlink from %s to %s',
                change[0],
                change[1]
            )
            try:
                os.remove(change[1])
                self.logger.info(
                    'Removed file at %s prior to linking',
                    change[1]
                )
            except:
                True

            try:
                os.symlink(change[0], change[1])
            except OSError as e:
                self.logger.error(
                    'Failed to create symlink from %s to %s: %s',
                    change[0],
                    change[1],
                    e
                )
