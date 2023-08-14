import React from 'react'
import ReactPaginate from 'react-paginate';

 function Paginate({list, size ,handlePageClick}) {
  return (
    <React.Fragment>
    {list ? (
        <div className="blog-content-section">
        <ReactPaginate
            nextLabel=">>"
            onPageChange={handlePageClick}
            pageRangeDisplayed={5}
            marginPagesDisplayed={2}
            pageCount={size}
            previousLabel="<<"
            pageClassName="page-item"
            pageLinkClassName="page-link text-decoration-none"
            previousClassName="page-item"
            previousLinkClassName="page-link"
            nextClassName="page-item"
            nextLinkClassName="page-link "
            breakLabel="..."
            breakClassName="page-item"
            breakLinkClassName="page-link"
            containerClassName="pagination"
            activeClassName="active"
            renderOnZeroPageCount={null}
        />
        </div>
    ) : (
        <div className="loading">Loading...</div>
    )}
    </React.Fragment>
  )
}

export default Paginate