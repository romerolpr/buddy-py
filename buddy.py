from Class import Compare, Screenshot
import cv2

try:

    compare = Compare()

    compare.load_container()

    compare.setOpenCV_methods((
        ("Correlation", cv2.HISTCMP_CORREL),
        ("Chi-Squared", cv2.HISTCMP_CHISQR),
        ("Intersection", cv2.HISTCMP_INTERSECT),
        ("Bhattacharyya", cv2.HISTCMP_BHATTACHARYYA)))

    compare.setOption("Correlation") # use this option

    # setting container json model
    compare.setJSONModel('\\Model\\inside_home.json')

    # compare.start_comparation()
    # compare.getResultNumber()

    screenshot = Screenshot()
    screenshot.curl_url('http://localhost/ricex.com.br/')

    # add new prop
    screenshot.add_props('wrapper', '.wrapper')
    # screenshot.add_props('section', 'section')
    # screenshot.add_props('footer_copyright', '.copyright-footer')

    screenshot.take_screenshot('wrapper', index=2)

    screenshot.take_screenshot('topo')
    screenshot.take_screenshot('banner')
    screenshot.take_screenshot('footer')
    screenshot.take_screenshot('mpi_home')
    screenshot.curl_url('http://localhost/ricex.com.br/alimentos-importados-da-italia')
    screenshot.take_screenshot('mpi_page_aside')
    screenshot.take_screenshot('mpi_page_region')
    screenshot.take_screenshot('mpi_page_breadcrumb')

    screenshot.kill()


except Exception as arg:
    print('Fatal error, cannot start class.', arg)

input('\nPress any key to close window...')