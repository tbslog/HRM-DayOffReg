import 'package:get/get.dart';
import 'en.dart';

import 'vi.dart';

class Messages extends Translations {
  @override
  Map<String, Map<String, String>> get keys => {
        'en_US': En().messages,
        'vi_VN': VI().messages,
      };
}
