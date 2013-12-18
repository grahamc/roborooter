
import FileHint
import os
import stat
import logging


class DeviceFile(FileHint.FileHint):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.hint_name = './manifests/devices'
        self.state_expression = r'^(.+)\s+(.+)$'
        self.rules = []

    def _filter_violations(self, path):
        for rule in self.rules:
            self.logger.debug('Testing rule: %s', rule)

            src_device = rule[0]
            target_device = os.path.join(path, rule[1])
            expected = self._extract_device_id(src_device)
            current = self._extract_device_id(target_device)
            if (expected != current):
                self.logger.info(
                    'Expected device file %s to have ID %s, but was %s',
                    target_device,
                    expected,
                    current
                )
                yield (src_device, target_device)

    def _extract_device_id(self, path):
        try:
            dev_stat = os.lstat(path)
            return dev_stat.st_rdev
        except OSError as e:
            self.logger.debug(
                'Failed to extract device ID from %s: %s',
                path,
                e
            )
            return None

    def _extract_device_mode(self, path):
        try:
            dev_stat = os.lstat(path)
            mode = 0
            if stat.S_ISBLK(dev_stat.st_mode):
                mode = stat.S_IFBLK
            elif stat.S_ISCHR(dev_stat.st_mode):
                mode = stat.S_IFCHR
            else:
                msg = 'File is not block or character: %s' % path
                self.logger.critical(msg)
                raise IOError(msg)

            return mode
        except OSError as e:
            self.logger.debug(
                'Failed to determine device mode of %s: %s',
                path,
                e
            )
            return None

    def fix(self, path):
        for change in self._filter_violations(path):
            if os.path.exists(change[1]):
                os.unlink(change[1])

            if not os.path.isdir(os.path.dirname(change[1])):
                os.makedirs(os.path.dirname(change[1]))

            self.logger.info(
                'Creating node at %s from %s',
                change[1],
                change[0]
            )
            dev_id = self._extract_device_id(change[0])
            dev_mode = self._extract_device_mode(change[0])
            try:
                os.mknod(change[1], dev_mode, dev_id)
            except OSError as e:
                self.logger.error(
                    'Failed to create node at %s: %s',
                    path,
                    e
                )
