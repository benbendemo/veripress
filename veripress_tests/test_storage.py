from pytest import raises

from veripress import app, create_app
from veripress.model import storage, get_storage
from veripress.model.storages import Storage, FileStorage
from veripress.helpers import ConfigurationError


def test_get_storage():
    wrong_app = create_app('config2.py')
    assert wrong_app.config['STORAGE_TYPE'] == 'fake_type'
    with raises(ConfigurationError, message='Storage type "fake_type" is not supported.'):
        with wrong_app.app_context():
            get_storage()  # this will raise a ConfigurationError, because the storage type is not supported

    with app.app_context():
        s = get_storage()
        assert storage == s
        assert id(storage) != id(s)
        # noinspection PyProtectedMember
        assert storage._get_current_object() == s

        assert isinstance(s, Storage)
        assert isinstance(s, FileStorage)
        assert s.config['STORAGE_TYPE'] == 'file'
    assert s.closed  # the storage object should be marked as 'closed' after the app context being torn down
    with raises(AttributeError):
        setattr(s, 'closed', True)


def test_fix_rel_url():
    with app.app_context():
        correct = '2017/01/01/my-post/'
        assert Storage.fix_post_relative_url('2017/01/01/my-post/') == correct
        assert Storage.fix_post_relative_url('2017/1/1/my-post') == correct
        assert Storage.fix_post_relative_url('2017/1/1/my-post.html') == correct
        assert Storage.fix_post_relative_url('2017/1/1/my-post/index') == correct + 'index.html'
        assert Storage.fix_post_relative_url('2017/1/1/my-post/index.html') == correct + 'index.html'
        assert Storage.fix_post_relative_url('2017/1/1/my-post/test') is None

        assert Storage.fix_page_relative_url('my-page') == ('my-page/', False)
        assert Storage.fix_page_relative_url('my-page/') == ('my-page/', False)
        assert Storage.fix_page_relative_url('test-page.txt') == ('test-page.txt', True)
        assert Storage.fix_page_relative_url('my-page/index.md') == ('my-page/index.md', True)
        assert Storage.fix_page_relative_url('my-page/index') == ('my-page/index.html', False)
        assert Storage.fix_page_relative_url('my-page/index.htm') == ('my-page/index.html', False)
        assert Storage.fix_page_relative_url('my-page/index.html') == ('my-page/index.html', False)
        assert Storage.fix_page_relative_url('//') == (None, False)

        assert Storage.fix_relative_url('post', '2017/1/1/my-post/index') == ('2017/01/01/my-post/index.html', False)
        assert Storage.fix_relative_url('page', '/my-page/index.htm') == ('my-page/index.html', False)
        with raises(ValueError, message='Publish type "wrong" is not supported'):
            Storage.fix_relative_url('wrong', 'wrong-publish-type/')


def test_base_storage():
    s = Storage(app.config)
    with raises(NotImplementedError):
        s.get_posts()
    with raises(NotImplementedError):
        s.get_post('')
    with raises(NotImplementedError):
        s.get_page('')
    with raises(NotImplementedError):
        s.get_widgets()
